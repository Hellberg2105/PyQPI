from NAMES import ControlPanel_name, ToolBar_name

from Plugin import Plugin
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QGridLayout,
    QRadioButton,
    QLineEdit,
    QFileDialog,
)

from PyQt5.QtGui import QFont


import numpy as np

import Singe_shot_py

import os
from PIL import Image
import threading
from tifffile import imsave

reconfolder_name = "Batch reconstruction"


class reconfolder(QWidget, Plugin):
    name = reconfolder_name

    def __init__(self):
        super().__init__()
        self.padding = 200
        self.oldimage = 0
        # self.pluginDict[InteractionHub_name].widget().addTab(self.interactionDisplay(), self.name)
        # currentIndex = self.pluginDict[InteractionHub_name].widget().currentIndex()
        # if currentIndex != 1:
        #     self.pluginDict[InteractionHub_name].widget().setCurrentIndex(currentIndex + 1)

    def setUp_launchButton(self):
        """
        When launch button clicked add a display in the interaction display

        """
        self.pluginDict[ControlPanel_name].widget().addTab(
            self.interactionDisplay(), self.name
        )
        currentIndex = self.pluginDict[ControlPanel_name].widget().currentIndex()
        if currentIndex != 1:
            self.pluginDict[ControlPanel_name].widget().setCurrentIndex(
                currentIndex + 1
            )

    def interactionDisplay(self):
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

        self.savelabel = QLabel("Save location:")
        self.savelabel.setFont(self.restfont)
        self.savelayout = QGridLayout()
        self.save_browse = QPushButton("Browse")
        self.save_browse.clicked.connect(self.browsesave)
        self.save_browse.setFont(self.restfont)
        self.savename_edit = QLineEdit()

        self.savelayout.addWidget(self.savelabel, 0, 0)
        self.savelayout.addWidget(self.savename_edit, 0, 1)
        self.savelayout.addWidget(self.save_browse, 0, 2)
        self.displaylayout.addLayout(self.savelayout, 1, 0)

        self.loadlabel = QLabel("Load folder:")
        self.loadlabel.setFont(self.restfont)
        self.loadlayout = QGridLayout()
        self.load_browse = QPushButton("Browse")
        self.load_browse.clicked.connect(self.browseload)
        self.load_browse.setFont(self.restfont)
        self.loadname_edit = QLineEdit()

        self.loadlayout.addWidget(self.loadlabel, 0, 0)
        self.loadlayout.addWidget(self.loadname_edit, 0, 1)
        self.loadlayout.addWidget(self.load_browse, 0, 2)
        self.displaylayout.addLayout(self.loadlayout, 1, 1)

        self.start_live_button = QPushButton()
        self.start_live_button.setText("start/stop reconstruction")
        self.start_live_button.clicked.connect(self.startrecon)
        self.start_live_button.setFont(self.Buttonsfont)
        self.displaylayout.addWidget(self.start_live_button, 1, 2, 1, 2)
        # print(QFont.defaultFamily())

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
        print(self.wavelength)

        # self.adv_tilt_removal = self.adv_tilt_checkbox.isChecked()

        self.window_size = self.window_spinbox.value()

    def browsesave(self):
        """
        Open an image file and display its contents in label widget.
        Display error message if image can't be opened.
        """
        self.savePath = QFileDialog.getExistingDirectory(self)
        self.savename_edit.setText(self.savePath)

    def browseload(self):
        """
        Open an image file and display its contents in label widget.
        Display error message if image can't be opened.
        """
        self.loadPath = QFileDialog.getExistingDirectory(self)
        self.loadname_edit.setText(self.loadPath)

    def startrecon(self):
        self.updatevalues()

        self.thread1 = threading.Thread(
            target=self.folderwalk, args=[self.savePath, self.loadPath]
        )
        self.condition = True
        self.thread1.setDaemon(True)
        self.thread1.start()

    def folderwalk(self, savelocation, loadlocation):
        cropp = 10

        for subdir, dirs, files in os.walk(loadlocation):
            i = 0
            for file in files:

                path_to_save = os.path.join(savelocation, file)
                path_to_file = os.path.join(subdir, file)
                imageorig = Image.open(path_to_file)
                image = np.array(imageorig)

                if i == 0:
                    mainfile = Singe_shot_py.main(1, image)

                printimage, window_size = mainfile.run(
                    image,
                    self.window_size,
                    self.FFT,
                    self.FFT_filter,
                    self.auto,
                    self.unwrap_method,
                    wavelength=self.wavelength,
                    pixel_size=self.pixel_size,
                )  # reconstruct image

                self.labeltext.setText("Current window size: " + str(window_size))

                x, y = np.shape(printimage)
                printimage = printimage[cropp : x - cropp, cropp : y - cropp]
                printimage = printimage.astype("float32")
                imsave(path_to_save, printimage, photometric="minisblack")
