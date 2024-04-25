import numpy as np


def ift_atan(fft_back, padding):
    """
    This is just the method for extracting the phase map.
    """

    # return np.arctan2(fft_back.imag,fft_back.real)
    return np.arctan2(fft_back.imag, fft_back.real)
