# PyQPI
## Introduction

The present plugin provides the open-source Python framework for the reconstruction of off-axis quantitative phase images. This software primarily focuses on reconstructing phase maps from various off-axis quantitative phase microscopy techniques, such as Mach-Zehnder interferometer, Tau interferometer, diffraction phase microscopy, shear plate-based interferometry, Linnik type interferometer. To effectively reconstruct phase maps, it is essential to ensure that the fringe density in the interferometric image is sufficiently high. This ensures the proper separation of the spatial frequencies of the sample and DC term in the Fourier domain image.

## Installation
To download the necessary files to run the plugin, users can use the link ([https://github.com/Hellberg2105/PyQPI/tags](https://github.com/Hellberg2105/PyQPI/tags) ). The PyQPI.exe file needs to be opened to use the tool. It can be used both with micro-manager for live reconstruction and for offline reconstruction.

## Usage

### Off-line reconstruction
For off-line reconstruction, “load folder” in the control panel will be used to load the location where the interferometric images are saved. Further, the users need to create new folder where they wish to save the final image and paste the location under the “save location” tab.

Users have the option to select automated window size for automatic selection of Fourier peak and Fourier filter size. Finally, users select the option between reconstruction, FFT, FFT filter to check the different reconstruction steps. Finally, users can select reconstruction and click the button “start/stop reconstruction”. The final image will be saved in the specified “save location”.

## Reconstruction with Micro-Manager
The ability to reconstruct interferograms taken directly from imaging can be done through Micro-Manager. The user needs to install Micro-Manager and capture images with it. Users should then either select automatic window size in PyQPI, or choose a window size that gives a good reconstruction. Pressing the "Do a single reconstruction" button will reconstruct the latest image taken in Micro-Manager. The user can also press the "start/stop live reconstruction" button to continuously reconstruct the latest images from Micro-Manager. This allows for live reconstruction of interferometric images captured with the microscope. 

## Unwrapping
Different unwrapping techniques can be chosen under file menu. The unwrapping techniques will be shown when hovering over the "unwrapping methods" section. Some unwrapping techniques require different parameters like pixel size and wavelength. These unwrapping methods will open a different settings window when chosen, where the user can input the parameters before applying the method. Under "file", the user can load their own image from the computer. Loading a wrapped image and choosing "unwrap image" from the "unwrapping methods" menu, will apply the selected unwrapping technique to the current image.

## Test data
Furthermore, we have provided some images acquired by different off-axis hologram in the folder "Images". Users may use these images to check the contrast of the interferogram and reconstruction steps.# PyQPI
