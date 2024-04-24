""" 
FileMenu

The standard menu to open and save files. 


Inspierd by 
https://github.com/Apress/beginning-pyqt/blob/master/ch05_MenusToolbarsAndMore/photo_editor.py
"""

# getting the names of relevant plugins
from NAMES import Main_name, ImageHandel_name, Display_name

# import the image backbone class

from Plugin import Plugin

# importing nesseary libraries
from PyQt5.QtWidgets import (
    QMenuBar,
    QAction,
    QFileDialog,
    QMessageBox,
    QPushButton,
    QWidget,
    QGridLayout,
    QSpinBox,
)
from PyQt5.QtGui import QFont

import Unwrappers


UNWRAP_MAPPING = {
    "skimage": Unwrappers.TIE_unwrap,
    "TIE": Unwrappers.unwrap,
}

Toolbar_name = "Toolbar"


class Toolbar(QMenuBar, Plugin):
    name = Toolbar_name

    def __init__(self):
        super().__init__()

        self.fileMenu = self.addMenu("File")
        self.unwrap_menu = self.fileMenu.addMenu("Unwrap method")
        self.selected_unwrap_method = "skimage"
        self.pixel_size = 0
        self.wavelength = 0
        self.setWindowTitle(self.name)

    def setUp_screenPosition(self):
        self.pluginDict[Main_name].setMenuBar(self)

    def setUp_actions(self):
        self.openAct = self.createOpenAct()
        self.skimage_unwrap = self.create_skimage_unwrap()
        self.TIE_unwrap = self.create_TIE_unwrap()
        self.apply_unwrap = self.create_apply_unwrap()

        # adding the open action to the file menu
        self.fileMenu.addAction(self.openAct)
        self.unwrap_menu.addAction(self.skimage_unwrap)
        self.unwrap_menu.addAction(self.TIE_unwrap)
        self.unwrap_menu.addAction(self.apply_unwrap)

    def createOpenAct(self):
        # creating a action to add to the file menu
        # icon =  QIcon('images/open_file.png')
        openAct = QAction("Open", self)
        openAct.setShortcut("Ctrl+O")
        openAct.setStatusTip("Open a new image")
        openAct.triggered.connect(self.openImage)
        return openAct

    def create_apply_unwrap(self):
        # creating ae action to add to the file menu
        unwrap_image = QAction("Unpwrap image", self)
        unwrap_image.setStatusTip("Apply selected unwrapping method")
        unwrap_image.triggered.connect(self.apply_unwrap)
        return unwrap_image

    def apply_unwrap(self):
        self.pluginDict[Display_name].currentWidget().setImage(
            UNWRAP_MAPPING[self.selected_unwrap_method](
                self.pluginDict[Display_name].currentWidget().npImage,
            )
        )

    def create_skimage_unwrap(self):
        # creating ae action to add to the file menu
        skimage_unwrap = QAction("Skimage unwrap", self)
        skimage_unwrap.setCheckable(True)
        skimage_unwrap.setStatusTip("Skimage's unwrapping method")
        skimage_unwrap.triggered.connect(self.set_skimage_unwrap)
        return skimage_unwrap

    def set_skimage_unwrap(self):
        self.uncheck_all()
        self.skimage_unwrap.setChecked(True)
        self.selected_unwrap_method = "skimage"

    def create_TIE_unwrap(self):
        # creating ae action to add to the file menu
        TIE_unwrap = QAction("TIE unwrap", self)
        TIE_unwrap.setCheckable(True)
        TIE_unwrap.setStatusTip("TIE unwrapping method")
        TIE_unwrap.triggered.connect(self.set_TIE_unwrap)
        return TIE_unwrap

    def set_TIE_unwrap(self):
        self.TIE_settings()
        self.TIE_setting_display.show()

    def TIE_settings(self):
        self.TIE_setting_display = QWidget()
        self.TIE_setting_display.setLayout(QGridLayout())

        self.TIE_setting_display_layout = QGridLayout()

        self.Buttonsfont = QFont("Sans Serif", 15)
        self.restfont = QFont("Sans Serif", 10)

        self.pixel_size_spinbox = QSpinBox()
        self.pixel_size_spinbox.setPrefix("Pixel size (nm): ")
        self.pixel_size_spinbox.setRange(1, 1000)
        self.pixel_size_spinbox.setFont(self.restfont)

        self.TIE_setting_display_layout.addWidget(self.pixel_size_spinbox, 0, 0, 1, 1)

        self.wavelength_spinbox = QSpinBox()
        self.wavelength_spinbox.setPrefix("Wavelength: ")
        self.wavelength_spinbox.setRange(1, 1000)
        self.wavelength_spinbox.setFont(self.restfont)
        self.TIE_setting_display_layout.addWidget(self.wavelength_spinbox, 0, 1, 1, 1)

        self.apply_button = QPushButton()
        self.apply_button.setText("Apply")
        self.apply_button.clicked.connect(self.apply_TIE_settings)
        self.apply_button.setFont(self.Buttonsfont)
        self.TIE_setting_display_layout.addWidget(self.apply_button, 1, 0, 2, 2)

        self.TIE_setting_display_layout.setRowStretch(4, 1)
        self.TIE_setting_display_layout.setSpacing(20)
        self.TIE_setting_display.layout().addLayout(
            self.TIE_setting_display_layout, 0, 0
        )

    def apply_TIE_settings(self):
        self.uncheck_all()
        self.TIE_unwrap.setChecked(True)
        self.selected_unwrap_method = "TIE"
        self.pixel_size = self.pixel_size_spinbox.value
        self.wavelength = self.wavelength_spinbox.value

    def uncheck_all(self):
        for action in self.unwrap_menu.actions():
            action.setChecked(False)

    def openImage(self):
        """
        Open an image file and display its contents in label widget.
        Display error message if image can't be opened.
        """
        imagePath, imageFileFormat = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "All files (*.*);; JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
           GIF Files (*.gif);; TIFF (*.tif)",
        )

        # making shure the file is opend correctly
        try:
            self.pluginDict[ImageHandel_name].openImage(imagePath, imageFileFormat)

        # display a error if not opend correctly
        except:
            QMessageBox.information(
                self, "Error", "Unable to open image.", QMessageBox.Ok
            )
