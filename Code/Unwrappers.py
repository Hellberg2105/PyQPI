from skimage.restoration import unwrap_phase
import numpy as np
from numpy import pi, fft


def skimage_unwrap(arctan, **kwargs):
    return unwrap_phase(arctan)


def TIE_unwrap(arctan, **kwargs):
    I1 = np.exp(1j * arctan)
    I2 = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(I1)))
    rows, cols = I1.shape

    # System parameters
    lambda_ = 660e-9
    p = 6.5e-6
    k = 2 * np.pi / lambda_
    z = 0e-3
    dz = 10e-9
    x, y = np.meshgrid(
        np.arange(-(rows // 2), (rows // 2)), np.arange(-cols // 2, cols // 2)
    )
    x = x * p
    y = y * p

    fx, fy = np.meshgrid(
        np.linspace(-1 / (2 * p), 1 / (p * rows) - 1 / (2 * p), cols),
        np.linspace(-1 / (2 * p), 1 / (p * rows) - 1 / (2 * p), rows),
    )

    # Angular spectrum transfer function
    f = fx**2 + fy**2
    h = np.sqrt(k**2 - 4 * pi**2 * f)
    H_positive = np.exp(1j * (z + dz) * h)
    H_negative = np.exp(1j * (z - dz) * h)

    # Convolution operation
    I3 = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(I2 * H_positive)))
    I4 = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(I2 * H_negative)))

    I2_1 = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(I2)))

    # Derivative of intensity
    I_deri = (np.abs(I3) ** 2 - np.abs(I4) ** 2) / (2 * dz)
    D0 = -4 * pi**2 * (fx**2 + fy**2)
    D = D0 / (D0**2 + 1e-12)
    I5 = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(I_deri)))
    phi_obj = -k * np.real(np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(I5 * D))))
    phi_obj -= np.min(phi_obj)
    return phi_obj


def unwrap(p, discont=127, axis=0, njumps_up=None, njumps_down=None):
    """A more generic unwrap function
    Parameters
    ----------
    p : array_like
        Input array.
    discont : float, optional
        Maximum discontinuity between values, default is ``127``.
    axis : int, optional
        Axis along which unwrap will operate, default is the last axis.
    njumps : int, optional
        Maximum number of discrepencies to correct

    >>> unwrap([0, 1, 2, 0], discont=1.5)
    array([0., 1., 2., 3.])
    >>> unwrap([2, 1, 0, 2], discont=1.5)
    array([ 2.,  1.,  0., -1.])
    >>> unwrap([0, 1, 2, 0, 1, 2, 0], discont=1.5)
    array([0., 1., 2., 3., 4., 5., 6.])
    >>> unwrap([0, 1, 2, 0, 1, 2, 0], discont=1.5, njumps_up=1)
    array([0., 1., 2., 3., 4., 5., 3.])
    >>> unwrap([2, 1, 0, 2], discont=1.5, njumps_down=0)
    array([2., 1., 0., 2.])
    """
    p = np.asarray(p)
    out = np.array(p, copy=True, dtype="d")
    # find the jumps
    dd = np.diff(p, axis=axis)
    ph_correct = np.zeros_like(dd)
    # undo the points that are too extreme

    if (njumps_up is not None) or (njumps_down is not None):
        ph_update = np.zeros(dd.shape)
        for i, idx in enumerate(zip(*np.where(dd < -discont))):
            if (njumps_up is not None) and (i >= njumps_up):
                break
            ph_update[idx] = 2 * discont

        for i, idx in enumerate(zip(*np.where(dd > discont))):
            if (njumps_down is not None) and (i >= njumps_down):
                break
            ph_update[idx] = -2 * discont

    else:
        dd[np.abs(dd) < discont] = 0
        ph_update = dd.copy()
        ph_update[dd > 0] = -2 * discont
        ph_update[dd < 0] = 2 * discont

    # update the right part of the array
    slice1 = [slice(None, None)] * p.ndim  # full slices
    slice1[axis] = slice(1, None)
    out[tuple(slice1)] = p[tuple(slice1)] + ph_update.cumsum(axis)
    return out
