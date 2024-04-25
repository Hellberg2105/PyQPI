from skimage.restoration import unwrap_phase
import numpy as np
import scipy.fft as fft


def skimage_unwrap(arctan, **kwargs):
    return unwrap_phase(arctan)


def numpy_unwrap(arctan, **kwargs):
    return np.unwrap(arctan)


def TIE_unwrap(phase1, **kwargs):
    I1 = np.exp(1j * phase1)
    I2 = fft.fftshift(fft.fft2(fft.fftshift(I1)))

    rows, cols = I1.shape

    # System parameters
    lambda_ = kwargs["wavelength"] * (10**-9)  # Wavelength
    p = kwargs["pixel_size"] * (10**-6)  # Pixel size
    k = 2 * np.pi / lambda_
    z = 0e-3  # Defocus distance
    dz = 10e-9

    x, y = np.mgrid[-(rows // 2) : (rows // 2), -(cols // 2) : (cols // 2)]

    x = x * p
    y = y * p

    fx, fy = np.mgrid[
        -1 / (2 * p) : 1 / (2 * p) : (1 / (p * rows)),
        -1 / (2 * p) : 1 / (2 * p) : (1 / (p * cols)),
    ]

    # Angular spectrum transfer function
    f = fx**2 + fy**2
    h = np.sqrt(k**2 - 4 * np.pi**2 * f)
    H_positive = np.exp(1j * (z + dz) * h)
    H_negative = np.exp(1j * (z - dz) * h)

    # Convolution operation
    I3 = fft.ifftshift(fft.ifft2(fft.ifftshift(I2 * H_positive)))
    I4 = fft.ifftshift(fft.ifft2(fft.ifftshift(I2 * H_negative)))

    # Intensity derivative
    I_deri = (np.abs(I3) ** 2 - np.abs(I4) ** 2) / (2 * dz)

    # Frequency filtering
    D0 = -4 * np.pi**2 * (fx**2 + fy**2)
    D = D0 / (D0**2 + np.finfo(float).eps)  # Handle potential division by zero

    I5 = fft.fftshift(fft.fft2(fft.ifftshift(I_deri)))
    phi_obj = -k * np.real(fft.ifftshift(fft.ifft2(fft.ifftshift(I5 * D))))

    # Normalize
    phi_obj = phi_obj - np.min(phi_obj)

    return phi_obj
