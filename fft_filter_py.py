import numpy as np
from scipy import ndimage


def create_circular_mask(h, w, center=None, radius=None):

    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


def operations(maxima_filtered, filter_matrix, fft_datatemp, width, height, limit):
    """
    Some basic operations for the fft filter method

    """

    cut_filter = maxima_filtered

    maxi = np.max(cut_filter)  # takes the max after cutting
    max_pos = np.where(cut_filter == maxi)  # position where cut filter is max

    max_pos_width = max_pos[1][len(max_pos[1]) // 2 :]  # calulating width
    max_pos_height = max_pos[0][len(max_pos[0]) // 2 :]  # calulating height

    max_pos_width = np.sort(max_pos[1])  # calulating width
    max_pos_height = np.sort(max_pos[0])  # calulating height

    height_window = int(np.median(max_pos_height))  # getting the median (middle)
    width_window = int(np.median(max_pos_width))  # getting the median (middle)

    window_size = limit

    x_before = width_window - window_size // 2  # calulate x values before
    x_after = width - width_window - window_size // 2  # calulate x values after

    y_before = height_window - window_size // 2  # calulate y values before
    y_after = height - height_window - window_size // 2  # calulate y values after
    return (
        y_before,
        y_after,
        x_before,
        x_after,
        width_window,
        height_window,
        window_size,
    )


def fft_filter(fft_datatemp, filter_matrix, limit, filterwindow):
    """
    main method to find peak and shift it

    """
    fft_datatemp_cut = np.multiply(filter_matrix, fft_datatemp)

    height, width = filter_matrix.shape  # gets the shape

    maxima_filtered = ndimage.maximum_filter(
        abs(fft_datatemp_cut), 50, mode="constant"
    )  # apply the maxima filter

    y_before, y_after, x_before, x_after, width_window, height_window, window_size = (
        operations(maxima_filtered, filter_matrix, fft_datatemp, width, height, limit)
    )  # do the operations method

    h, w = fft_datatemp.shape[:2]  # gettign the shape

    hamming = create_circular_mask(window_size, window_size)

    window_matrix = np.pad(
        hamming, [(y_before, y_after), (x_before, x_after)], mode="constant"
    )  # pad the window to the size of the image

    windowed_data_orig = np.multiply(
        window_matrix, fft_datatemp
    )  # multiply so that only the peaks where the window is is kept

    if filterwindow:
        return (
            abs(windowed_data_orig),
            window_size,
        )  # returns if the printing condition is the filtered window

    windowed_data = np.roll(
        windowed_data_orig, int(abs(width_window - width // 2)), axis=1
    )  # roll back to the center in x direction
    windowed_data = np.roll(
        windowed_data, int(-abs(height_window - height // 2)), axis=0
    )  # roll back to the center in y direction

    return windowed_data, window_size
