"""
This module contains the Piece class.
"""
#pylint: disable=R0913,R0917


import typing as t
import numpy as np


class Piece:
    """
    This represents a piece on the board.
    """

    def __init__(self, uuid: int, name: str, text_color: str, gui_colour: t.List[float],
                 default_mask: t.List[t.List[bool]]) -> None:
        """
        Initialize the piece with the given color and positions.

        :param uuid: The unique identifier for the piece.
        :param name: Name of the piece.
        :param text_color: Colour of the piece.
        :param gui_colour: Colour of the piece in the GUI.
        :param default_mask: A 2D mask of the peice as bools.
        eg [[True, False], [True, True]] is a 90deg corner.
        """
        self.__text_color: str = text_color
        self.__gui_colour = gui_colour
        self.__masks = []
        self.__name = name
        self.__uuid = uuid

        for flip in [True, False]:
            for rotation in [0, 1, 2, 3]:
                new_mask = np.array(default_mask)
                new_mask = np.fliplr(new_mask) if flip else new_mask
                new_mask = np.rot90(new_mask, rotation)

                if not self.mask_exists(new_mask):
                    self.__masks.append(new_mask)

    def mask_exists(self, new_mask):
        """
        Determines if the given mask is identical to any existing generated
        mask for this game piece.

        :param new_mask: new mask for comparison
        :return: True if given mask is identical to any existing mask, else False.
        """

        return any(np.array_equal(new_mask, m) for m in self.__masks)

    def get_masks(self):
        """
        Get the masks for the piece.

        :return: The masks for the piece.
        """
        return self.__masks

    def get_uuid(self) -> int:
        """
        Get the UUID of the piece.

        :return: The UUID of the piece.
        """
        return self.__uuid

    def get_name(self) -> str:
        """
        Get the name of the piece.

        :return: The name of the piece.
        """
        return self.__name

    def get_color(self) -> str:
        """
        Get the color of the piece.

        :return: The color of the piece.
        """
        return self.__text_color

    def __str__(self) -> str:
        """
        String representation of the piece.

        :return: Return a string representation of the piece
        """
        return f"Board piece - Name:{self.__name}, UUID:{self.__uuid}, Colour:{self.__gui_colour}"
