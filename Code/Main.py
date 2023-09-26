""" MainWindow

In this file is the main windo which has the main loop responsible for 
handeling the application. 

All the plugins is importet from the PluginManager and launched here.
 """
import sys
from qdarkstyle import load_stylesheet_pyqt5
from PyQt5.QtWidgets import  QMainWindow, QApplication
from Manager import Manager


from NAMES import  ImageHandel_name



Main_name = 'Main'

class Main(QMainWindow):
    name = Main_name

    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000,750)
        
        # creating the pluginmaneger wich store all the diffrent plugins 
        self.pluginManager = Manager()  
        self.pluginDict = self.pluginManager.plugins
        
               
        # launching each plugin in the plugin manger 
        for plugin_name in self.pluginManager.plugins: 
            if plugin_name == self.name :
                
                #seting up the main window object 
                self.pluginManager.plugins[plugin_name] = self
            else:
                # making a short referance to help referencing the objects 
                obj = self.pluginManager.plugins[plugin_name] 
                
                # Seting up the diffrent objects, positions and actions
                # all the functions called is found in PluginBackBone
                obj.setUp_pluginDict(self.pluginManager.plugins)
                obj.setUp_screenPosition()
                obj.setUp_actions()
                obj.setUp_launchButton()
                
                #printint for erorr handeling 
                print(obj)


        self.pluginDict[ImageHandel_name].openImage(r'D:\remotedesk\Code_phase_Reconstruction\gui\black.png', 'png')

        self.setWindowTitle("PyQPI")

    
    
            
        


    
# Startin the application 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    mainWindow = Main()
    mainWindow.show()
    app.exec_()

        