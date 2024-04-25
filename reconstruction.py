from NAMES import ControlPanel_name, Display_name, ToolBar_name

from Plugin import Plugin
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QRadioButton,
)

from PyQt5.QtGui import QFont
from pycromanager import Core
from matplotlib.pyplot import cm

import numpy as np

import Singe_shot_py

from PIL import Image


import threading

liverecon_name = "Live recostruction"


class reconstruction(QWidget, Plugin):
    name = liverecon_name

    def __init__(self):
        super().__init__()
        self.padding = 200
        self.oldimage = 0
        self.cmap = cm.get_cmap("jet")
        # self.launchAction()

    def setUp_launchButton(self):
        """
        When launch button clicked add a display in the interaction display

        """
        self.pluginDict[ControlPanel_name].widget().addTab(
            self.manualinteractionDisplay(), self.name
        )
        currentIndex = self.pluginDict[ControlPanel_name].widget().currentIndex()
        if currentIndex != 1:
            self.pluginDict[ControlPanel_name].widget().setCurrentIndex(
                currentIndex + 1
            )

    def manualinteractionDisplay(self):
        self.display = QWidget()
        self.display.setLayout(QGridLayout())

        self.displaylayout = QGridLayout()

        self.Buttonsfont = QFont("Sans Serif", 15)
        self.restfont = QFont("Sans Serif", 10)

        self.combobox = QComboBox()
        self.combobox.addItem("Reconstruction")
        self.combobox.addItem("FFT")
        self.combobox.addItem("FFT filter")
        self.combobox.setFont(self.restfont)
        self.displaylayout.addWidget(self.combobox, 0, 0)

        self.manuallayout = QHBoxLayout()
        self.manual_window_size = QRadioButton("Manual window size:")
        self.manual_window_size.setChecked(True)
        self.manual_window_size.setFont(self.restfont)
        self.manuallayout.addWidget(self.manual_window_size)

        self.window_spinbox = QSpinBox()
        self.window_spinbox.setRange(1, 1000)
        self.window_spinbox.setValue(200)
        self.window_spinbox.setFont(self.restfont)
        self.manuallayout.addWidget(self.window_spinbox)

        self.displaylayout.addLayout(self.manuallayout, 0, 1)

        self.auto_window_size = QRadioButton("Automatic window size")
        self.auto_window_size.setFont(self.restfont)
        self.displaylayout.addWidget(self.auto_window_size, 0, 2)

        self.labeltext = QLabel("Current window size:")
        self.labeltext.setFont(self.restfont)
        self.displaylayout.addWidget(self.labeltext, 0, 3, 1, 1)

        self.single_recon_button = QPushButton()
        self.single_recon_button.setText("Do a single reconstruction")
        self.single_recon_button.clicked.connect(self.single_recon)
        self.single_recon_button.setFont(self.Buttonsfont)
        self.displaylayout.addWidget(self.single_recon_button, 1, 0, 2, 2)

        self.start_live_button = QPushButton()
        self.start_live_button.setText("start/stop live reconstruction")
        self.start_live_button.clicked.connect(self.start_live_recon)
        self.start_live_button.setFont(self.Buttonsfont)
        self.start_live_button.setCheckable(True)
        self.displaylayout.addWidget(self.start_live_button, 1, 2, 2, 2)

        self.displaylayout.setRowStretch(4, 1)
        self.displaylayout.setSpacing(20)
        self.display.layout().addLayout(self.displaylayout, 0, 0)

        return self.display

    def updatevalues(self):
        if self.combobox.currentText() == "Reconstruction":
            self.FFT = False
            self.FFT_filter = False
        elif self.combobox.currentText() == "FFT":
            self.FFT = True
            self.FFT_filter = False
        elif self.combobox.currentText() == "FFT filter":
            self.FFT = False
            self.FFT_filter = True
        if self.auto_window_size.isChecked():
            self.auto = True
        if self.manual_window_size.isChecked():
            self.auto = False
        self.unwrap_method = self.pluginDict[ToolBar_name].selected_unwrap_method
        self.pixel_size = self.pluginDict[ToolBar_name].pixel_size
        self.wavelength = self.pluginDict[ToolBar_name].wavelength

        # self.adv_tilt_removal = self.adv_tilt_checkbox.isChecked()

        self.window_size = self.window_spinbox.value()

    def Getimage(self):
        try:
            core = Core()
            tagged_image = core.get_tagged_image()  # gets latest image
            image_height = tagged_image.tags["Height"]  # gets height of image
            image_width = tagged_image.tags["Width"]  # gets Width of image
            self.newimage = np.asarray(
                tagged_image.pix.reshape((image_height, image_width))
            )  # reshapes the image
        except:
            print("No connection to Micro-manager found")
            self.newimage = self.oldimage

    def single_shot(self):

        currentWidget = self.pluginDict[Display_name].currentWidget()
        self.Getimage()

        if np.array_equal(self.oldimage, self.newimage) == True:
            return

        if np.shape(self.oldimage) != np.shape(self.newimage):
            mainfile = Singe_shot_py.main(self.padding, self.newimage)

        self.updatevalues()

        Numpyimage, window_size = mainfile.run(
            self.newimage,
            self.window_size,
            self.FFT,
            self.FFT_filter,
            self.auto,
            self.unwrap_method,
            wavelength=self.wavelength,
            pixel_size=self.pixel_size,
        )  # reconstruct image

        crop = 10
        x, y = Numpyimage.shape
        Numpyimage = Numpyimage[crop : x - crop, crop : y - crop]

        self.labeltext.setText("Current window size: " + str(window_size))

        currentWidget.UpdateImage(npImage=Numpyimage)
        self.oldimage == self.newimage

    def single_recon(self):

        self.single_shot()

    def start_live_recon(self):
        if self.start_live_button.isChecked() == True:
            self.thread1 = threading.Thread(target=self.endlessloop, args=[])
            self.condition = True
            self.thread1.setDaemon(True)
            self.thread1.start()

        else:
            self.condition = False

        # self.endlessloop()

    def stop_live_recon(self):
        self.condition = False

    def endlessloop(self):
        while self.condition:

            # thread1 = threading.Thread(target=self.single_shot, args=[])
            self.single_shot()

            # thread1.start()
            # thread1.join()
            # time.sleep(3)

        # self.thread1.join(3)
