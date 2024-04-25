""" 
ControlPanel

The idea of the ControlPanel is to surve as a Hub for controlling all the
diffrent plugins. When a plugin is launched, the part of the plugin which 
has to do with ajusting parameters and so on. Will be displayed in this Q Dock 
Widget. 
"""

# geting the name of relevatn plugins
from NAMES import Main_name

# importing nesseary libraries
from PyQt5 import QtCore
from Plugin import Plugin
from PyQt5.QtWidgets import QDockWidget, QTabWidget


ControlPanel_name = "Control panel"


class ControlPanel(QDockWidget, Plugin):
    name = ControlPanel_name

    def __init__(self):
        super().__init__()
        self.setMinimumSize(100, 20)

        self.setFixedHeight(150)

        self.setWindowTitle(self.name)
        self.setWidget(QTabWidget())

        self.widget().setMovable(False)

        self.widget().setTabsClosable(False)

    def setUp_screenPosition(self):
        self.pluginDict[Main_name].addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
