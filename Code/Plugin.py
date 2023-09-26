""" PluginBackBone 

The idea is to have a backbone to each plugin since some functionality will 
be used over and over again. 

All the setUp functions will be called in the main window when the app is 
launched. If the functionality is relevant for the plugin you are making. The 
this function has to be overwritten.  


"""

# importing nesseary libraries 
from PyQt5.QtCore import QObject

Plugin_name  = 'Plugin'
class Plugin(QObject):
    name = Plugin_name
    def __init__(self):
        super().__init__()
        


        
    def setUp_pluginDict(self, pluginDict):
        """ Evry plugin will refere to other plugins throuh the 
        plugin dictionary, pluginDict. 
        
        input: 
            The input is the Pluginmanager.plugin dictionary from 
            the PluginManager class"""
        
        self.pluginDict = pluginDict
        
    def setUp_screenPosition(self): 
        """ Seting up the position on the main window screen  """
        pass
    def setUp_actions(self): 
        """ Launching all the relevant actions for launching the 
        plugin """
        pass
    
    def setUp_launchButton(self):
        """ Setting up launch button for launching the 
        plugin """
        pass