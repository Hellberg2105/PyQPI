import numpy as np


def tilt_removal(image, advanced):
    """
    This is the method that applies the tilt correction. It takes the image and a condition for advanced tilt correction and returns the corrected image.
    """

    order = 2
    xshape, yshape = np.shape(image)  # extracts the shape of the image

    if advanced == True:  # checks if the tilt correction is advanced or not
        samples = 200  # how many lines for each axis is used to apply correction

        y1 = image[xshape - 1, :]  # gets the first line in x direction
        x1 = np.arange(0, len(y1), 1)  # gets x values
        z1 = np.polyfit(x1, y1, order)  # applies a curve fitting.

        for x in range(1, samples):  # loop through samples

            y1 = image[
                xshape - x * xshape // samples, :
            ]  # calculates the vectors given sample
            z1 += np.polyfit(x1, y1, order)  # adding the curve fit with the others

        z1 = z1 / samples  # here an average curve is calculated

        p = np.poly1d(z1)  # creates the correction curve array

        # next the step is repeated in the other axis
        y2 = image[:, yshape - 1]

        x2 = np.arange(0, len(y2), 1)
        z2 = np.polyfit(x2, y2, order)

        for x in range(1, samples):
            y2 = image[:, yshape - x * yshape // samples]
            z2 += np.polyfit(x2, y2, order)

        z2 = z2 / samples

        p2 = np.poly1d(z2)
    else:  # if advanced correction is turned of

        y1 = image[xshape // 2, :]  #
        x1 = np.arange(0, len(y1), 1)
        z1 = np.polyfit(x1, y1, 2)

        p = np.poly1d(z1)

        y2 = image[:, yshape // 2]

        x2 = np.arange(0, len(y2), 1)
        z2 = np.polyfit(x2, y2, 2)

        p2 = np.poly1d(z2)

    x_correction = np.asmatrix(
        np.fromfunction(p, (len(y1),))
    )  # calculates the x direction correction
    y_correction = np.asmatrix(
        np.fromfunction(p2, (len(y2),))
    )  # calculates the y direction correction

    ones1 = np.asmatrix(np.ones(len(y2)))  # for matrix creation
    ones2 = np.asmatrix(np.ones(len(y1)))  # for matrix creation

    matrix1 = y_correction.T * ones2  # creates the matrix from correction
    matrix2 = ones1.T * x_correction  # creates the matrix from correction

    matrix_tot = matrix1 + matrix2  # total correction matrix

    image_untilted = image - matrix_tot  # subtract from image

    return image_untilted
