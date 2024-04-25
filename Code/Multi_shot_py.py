import numpy as np

from skimage.restoration import unwrap_phase
import Tilt_removal_py


def multishot(edata1, edata2, edata3, edata4, edata5, advanced):
    div = np.divide(2 * (edata4 - edata2), edata1 - 2 * edata3 + edata5)
    div[np.isinf(div)] = np.pi / 2
    div[np.isnan(div)] = 0

    phase = np.arctan(div)
    data_unwrap = unwrap_phase(phase)
    image_untilted = Tilt_removal_py.tilt_removal(data_unwrap, advanced)
    return image_untilted
