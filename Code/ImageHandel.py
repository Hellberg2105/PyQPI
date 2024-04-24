""" ImageBackBone 

a class to store the images as numpy arrays
"""

from PIL import Image
import numpy as np
from NAMES import Display_name

from Plugin import Plugin
import os

from pyqtgraph import ImageView


class ImageHandel(ImageView, Plugin):
    name = "ImageBackBone"

    def __init__(self):
        super().__init__()

    def update(self, fileFormat, fileName, imagePath):
        self.fileFormat = fileFormat
        self.fileName = fileName
        self.imagePath = imagePath
        self.pilImage = Image.open(self.imagePath)
        self.npImage = np.asarray(self.pilImage)

    def Updatenumpy(self, npImage):
        self.npImage = npImage

    def npImageToPIL(self, npImage):
        self.npImage = npImage
        self.pilImage = Image.fromarray(npImage)

    def UpdatePIL(self, pilImage):
        self.pilImage = pilImage
        self.npImage = np.asarray(pilImage)

    def openImage(self, imagePath, imageFileFormat):
        # getting the name of the file, need it for the tab name

        imageFileName = os.path.basename(imagePath)

        new = ImageHandel()
        new.update(imageFileFormat, imageFileName, imagePath)

        new.setImage(new.npImage)

        new.setUp_pluginDict(self.pluginDict)

        # displaying the image as a tab in the central widget
        self.pluginDict[Display_name].addTab(new, imageFileName)
        currentIndex = self.pluginDict[Display_name].currentIndex()
        self.pluginDict[Display_name].setCurrentIndex(currentIndex + 1)

    def UpdateImage(self, npImage=None):
        if npImage is not None:
            self.npImageToPIL(npImage)

        self.setImage(self.npImage)
