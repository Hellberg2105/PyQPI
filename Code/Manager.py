""" PluginManager """

from NAMES import *

from Display import Display
from ControlPanel import ControlPanel
from Toolbar import Toolbar
from ImageHandel import ImageHandel
from reconstruction import reconstruction
from reconfolder import reconfolder


from PyQt5.QtCore import QObject

Manager_name = "Manager"


class Manager(QObject):
    """Global plugin registry"""

    name = "Manager"

    def __init__(self):
        super().__init__()
        self.plugins = {
            Main_name: None,
            Display_name: Display(),
            ControlPanel_name: ControlPanel(),
            ToolBar_name: Toolbar(),
            ImageHandel_name: ImageHandel(),
            reconstruction: reconstruction(),
            reconfolder: reconfolder(),
        }
