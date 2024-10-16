"""
This module reads in an image of a Genius Square board and pieces,
and processes it to create a board object.
"""

# pylint: disable=E1101, R0914


from copy import deepcopy
import cv2
import numpy as np


class ImageReader:
    """
    This class reads in an image of a Genius Square board and pieces.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize the ImageReader object.

        :param path: The path to the image file.
        """
        self.__path = path
        self.__transform_matrix = None  # This will be the transform matrix used later
        self.__marker_names = []  # This holds the names of the markers eg A1, B2 etc
        self.__image = None  # This will hold the processed image

    def get_image(self) -> np.array:
        """
        Get the processed image.

        :return: The processed image.
        """
        return deepcopy(self.__image)

    def get_marker_names(self) -> list[str]:
        """
        Get the marker names.

        :return: The marker names.
        """
        return self.__marker_names

    def process(self) -> None:
        """
        This function processes the image to create a list of pieces in it.
        """

        raw_image = cv2.imread(self.__path, cv2.IMREAD_COLOR)

        # Convert to grayscale.
        gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

        # Blur using 10 * 10 kernel.
        kernel_size = 10
        gray_blurred = cv2.blur(gray, (kernel_size, kernel_size))

        # find the blockers and orientation markers using HoughCircles
        blockers = cv2.HoughCircles(gray_blurred,
                                    cv2.HOUGH_GRADIENT, 1, 100, param1=50,
                                    param2=40, minRadius=100, maxRadius=200)

        orientation_markers = cv2.HoughCircles(gray_blurred,
                                               cv2.HOUGH_GRADIENT, 1, 100, param1=50,
                                               param2=40, minRadius=30, maxRadius=100)

        blockers = np.uint16(np.around(blockers))
        orientation_markers = np.uint16(np.around(orientation_markers))

        # Throw errors if the number of blockers or orientation markers is not correct
        if blockers is None or len(blockers[0, :]) != 7:
            raise ValueError("There should be 7 blockers")
        if orientation_markers is None or len(orientation_markers[0, :]) != 3:
            raise ValueError("There should be 3 orientation markers")

        orientation_marker_radius = int(orientation_markers[0][0][2])

        corner, ax_up, ax_right = self.__calculate_axes(orientation_markers)

        warped_image = self.__calculate_4_transform(raw_image, np.array(
            [corner, corner + ax_up, corner + ax_right, corner + ax_up + ax_right]))

        # warp orientation markers So they have new positions in the warped image
        new_markers = []
        for pt in [corner, corner + ax_up, corner + ax_right, corner + ax_up + ax_right]:
            a, b, r = pt[0], pt[1], orientation_marker_radius
            p = np.array([[a, ],
                          [b],
                          [1]])
            p = np.matmul(self.__transform_matrix, p)
            # get point name
            cv2.circle(warped_image, (int(p[0, 0]), int(p[1, 0])), r, (0, 0, 255), 10)
            new_markers.append((int(p[0, 0]), int(p[1, 0]), r))

        # Get the max and min x & y values of the new markers so we can find what square of the
        # board a circle is in
        x_range = (min(new_markers, key=lambda x: x[0])[0], max(new_markers, key=lambda x: x[0])[0])
        y_range = (min(new_markers, key=lambda x: x[1])[1], max(new_markers, key=lambda x: x[1])[1])

        # Get the new positions of the blockers, draw them and calculate the names of the markers
        for pt in blockers[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            p = np.array([[a, ],
                          [b],
                          [1]])
            p = np.matmul(self.__transform_matrix, p)
            # get point name

            x_co = round(self.__remap(int(x_range[0]) + 200,
                                      int(x_range[1]) - 200, 1, 6, int(p[0, 0])))
            y_co = round(self.__remap(int(y_range[0]) + 200,
                                      int(y_range[1]) - 200, 0, 5, int(p[1, 0])))
            name = f'{"ABCDEF"[int(y_co)]}{x_co}'
            self.__marker_names.append(name)

            # draw the blocker
            cv2.circle(warped_image, (int(p[0,0]), int(p[1,0])), r, (255, 0, 0), 5)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(warped_image, (int(p[0,0]), int(p[1,0])), 1, (255, 0, 0), 10)
            cv2.putText(warped_image, name, (int(p[0,0]) - 20, int(p[1,0])), cv2.FONT_ITALIC,
                        2, (0, 0, 255), 3, cv2.LINE_AA)

        self.__image = warped_image

    @staticmethod
    def __calculate_axes(orientation_markers: np.array) -> tuple[np.array, np.array, np.array]:
        """
        This function calculates the axis of the board based on the orientation markers.

        :param orientation_markers: The orientation markers.

        :return: The corner, the up axis and the right axis.
        """
        a = np.array([int(orientation_markers[0, 0][0]), int(orientation_markers[0, 0][1])])
        b = np.array([int(orientation_markers[0, 1][0]), int(orientation_markers[0, 1][1])])
        c = np.array([int(orientation_markers[0, 2][0]), int(orientation_markers[0, 2][1])])
        ab = b - a
        ac = c - a
        bc = c - b
        adot = abs(np.dot(ab, ac))
        bdot = abs(np.dot(ab, bc))
        cdot = abs(np.dot(ac, bc))

        if min(adot, bdot, cdot) == adot:
            corner = a
            ax_up = ac
            ax_right = ab
        elif min(adot, bdot, cdot) == bdot:
            corner = b
            ax_up = -ab
            ax_right = bc
        else:
            corner = c
            ax_up = -bc
            ax_right = -ac

        return corner, ax_up, ax_right

    @staticmethod
    def __order_points(pts: np.array) -> np.array:
        """
        initialises a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        NB this code is from pyimagesearch.com

        :return: The ordered array of coordinates.
        """

        rect = np.zeros((4, 2), dtype="float32")
        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        # return the ordered coordinates
        return rect

    def __calculate_4_transform(self, image, pts):
        """
        This function transforms an image so the 4 pts are in the corners
        It also sets the transform matrix for later use.
        NB: This code is from pyimagesearch.com

        :param image: the image to warp
        :param pts: The 4 points to warp to
        :return: The warped image
        """
        # obtain a consistent order of the points and unpack them
        # individually
        rect = self.__order_points(pts)
        (tl, tr, br, bl) = rect
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b))
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b))
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]], dtype="float32")
        # compute the perspective transform matrix and then apply it
        matrix = cv2.getPerspectiveTransform(rect, dst)
        self.__transform_matrix = matrix
        warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
        # return the warped image
        return warped

    @staticmethod
    def __remap(in_min: float, in_max: float, out_min: float, out_max: float, v: float) -> float:
        """
        Remaps a value from one range to another.

        :param in_min: minimum value of the input range.
        :param in_max: maximum value of the input range.
        :param out_min: minimum value of the output range.
        :param out_max: maximum value of the output range.
        :param v: The value to remap.

        :return: The remapped value.
        """
        return (1 - ((v - in_min) / (in_max - in_min))) * out_min + (
                (v - in_min) / (in_max - in_min)) * out_max


if __name__ == "__main__":
    reader = ImageReader('../res/test2.jpg')
    reader.process()
    print(reader.get_marker_names())
    cv2.imshow("Image", reader.get_image())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
