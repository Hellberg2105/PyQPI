
""" 
FileMenu

The standard menu to open and save files. 


Inspierd by 
https://github.com/Apress/beginning-pyqt/blob/master/ch05_MenusToolbarsAndMore/photo_editor.py
"""
# getting the names of relevant plugins
from NAMES import Main_name,ImageHandel_name

# import the image backbone class

from Plugin import Plugin

# importing nesseary libraries 
from PyQt5.QtWidgets import (QMenuBar, QAction, QFileDialog, QMessageBox) 


Toolbar_name = 'Toolbar'
        
class Toolbar(QMenuBar,Plugin):
    name = Toolbar_name
    def __init__(self):
        super().__init__()
        
        self.fileMenu = self.addMenu('File')
        
        self.setWindowTitle(self.name)  


    def setUp_screenPosition(self): 
        self.pluginDict[Main_name].setMenuBar(self)
    
    def setUp_actions(self):
        self.openAct = self.createOpenAct()


        
        #adding the open action to the file menu 
        self.fileMenu.addAction(self.openAct)
        



    
    def createOpenAct(self):
        # creating a action to add to the file menu
        #icon =  QIcon('images/open_file.png')
        openAct = QAction("Open", self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open a new image')
        openAct.triggered.connect(self.openImage)
        return openAct


            
    
    def openImage(self):
        """
        Open an image file and display its contents in label widget.
        Display error message if image can't be opened. 
        """
        imagePath, imageFileFormat  = QFileDialog.getOpenFileName(self, "Open Image",
           "", "All files (*.*);; JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
           GIF Files (*.gif);; TIFF (*.tif)")

        # making shure the file is opend correctly 
        try:
            self.pluginDict[ImageHandel_name].openImage(imagePath, imageFileFormat)
            
        
        # display a error if not opend correctly 
        except:
            QMessageBox.information(self, "Error", 
                                    "Unable to open image.", QMessageBox.Ok)
            
  

    
    
        
        
        

        
    
            
        
