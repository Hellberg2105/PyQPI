import numpy as np


import fft_filter_py
import fft_filter_auto_py

import ift_atan_py
import Unwrappers

import Tilt_removal_py

UNWRAP_MAPPING = {
    "skimage": Unwrappers.skimage_unwrap,
    "numpy": Unwrappers.numpy_unwrap,
    "TIE": Unwrappers.TIE_unwrap,
}


class main:
    def __init__(self, padding, edata):
        """
        This is where the class is initialized and the basic setup is done

        Parameters
        ----------
        padding : int
            The padding of the data
        edata : matrix
            The image to be initalzied.

        Returns
        -------
        None.

        """
        self.padding = padding  # sets pading
        edata = np.double(edata)  # makes data type double

        edata = np.pad(
            edata, [(self.padding,), (self.padding,)], mode="constant"
        )  # pad the image
        self.height, self.width = edata.shape  # get the shape
        self.width_array2 = np.zeros(
            self.width // 2 + 80
        )  # array for creating cutting matrix
        self.width_array1 = np.ones(self.width // 2 - 80)  # same as above

        self.width_array = np.asmatrix(
            np.concatenate((self.width_array1, self.width_array2))
        )  # creating the cutting matrix to be used later

        self.height_array2 = np.ones(
            self.height
        )  # for creating cutting matrix. Is not really needed for no cutting in height
        self.height_array = np.asmatrix(self.height_array2)
        self.filter_matrix = (
            self.height_array.T @ self.width_array
        )  # taking the two matrixes and taking element multiplication.

    def run(self, edata, windowsize, FFT, filterwindow, auto, Unwrap_method, **kwargs):
        """
        This is the main reconstruction function.

        Parameters
        ----------
        edata : matrix
            The image to be reconstructed.
        windowsize : int
            Size of the window for the filter.
        FFT : bool
            If the FFT is to be returned.
        filterwindow : bool
            If the filterwindow is to be returned..
        advanced : bool
            If there should be advanced tilt correction.

        Returns
        -------
        matrix
            Reconstructed image, FFT or filtered window.

        """
        edata = np.double(edata)  # double type
        datawidth, dataheight = edata.shape

        if auto:
            fft = fft_filter_auto_py
        else:
            fft = fft_filter_py

        cosx = np.cos(np.linspace(-np.pi / 2, np.pi / 2, datawidth))
        cosy = np.cos(
            np.linspace(-np.pi / 2, np.pi / 2, dataheight)
        )  # calculate hamming window the other direction
        cos = np.outer(cosx, cosy)  # create the window
        edata = np.multiply(edata, cos)
        edata = np.pad(
            edata, [(self.padding,), (self.padding,)], mode="constant"
        )  # pads the data

        fft_data = np.fft.fftshift(np.fft.fft2(edata))  # calculate fft
        if FFT:
            return np.log(abs(fft_data) + 1), 0  # returns fft
        if filterwindow:
            filtered, window_size = fft.fft_filter(
                fft_data, self.filter_matrix, windowsize, filterwindow
            )
            return np.log(abs(filtered) + 1), filterwindow  # returns filterwindo

        windowed_data, window_size = fft.fft_filter(
            fft_data, self.filter_matrix, windowsize, False
        )  # applies filter

        fft_back = np.fft.ifft2(np.fft.fftshift(windowed_data))  # takes the fft back
        arctan = ift_atan_py.ift_atan(fft_back, self.padding)[
            self.padding : -self.padding, self.padding : -self.padding
        ]  # extract phase

        from tifffile import imsave

        imsave("E:\\test.tiff", arctan, photometric="minisblack")
        ifft_unwrapped = UNWRAP_MAPPING[Unwrap_method](
            arctan, wavelength=kwargs["wavelength"], pixel_size=kwargs["pixel_size"]
        )  # unwrap phase
        image_untilted = Tilt_removal_py.tilt_removal(
            ifft_unwrapped, True
        )  # tilt removeal

        return image_untilted, window_size
