""" CentralWidget

This widget will display the images and the reults of each operation done on 
the images.
 """

# getting the names of relevant plugins
from NAMES import Main_name


# importing nesseary libraries
from Plugin import Plugin
from PyQt5.QtWidgets import QTabWidget

Display_name = "Display"


class Display(QTabWidget, Plugin):
    name = Display_name

    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.name)

        self.setMovable(True)

        self.setTabsClosable(False)

    def setUp_screenPosition(self):
        self.pluginDict[Main_name].setCentralWidget(self)
