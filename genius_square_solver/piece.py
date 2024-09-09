"""
This module contains the Piece class.
"""
import typing as t


class Piece:
    """
    This represents a piece on the board.
    """

    def __init__(self, color: str, positions: t.List[t.Tuple[int, int]]) -> None:
        """
        Initialize the piece with the given color and positions.

        :param color: Colour of the piece.
        :param positions: Relative positions of the piece.
               from the top left corner, going right and down.
        """
        self.__color: str = color
        self.__relative_positions: t.List[t.Tuple[int, int]] = positions

        self.__position: t.Tuple[int, int] = (0, 0)
        self.__rotation: int = 0  # 0, 1, 2, 3 (0 is no rotation, 1 is 90 degrees, etc.)

    def set_position(self, x: int, y: int) -> None:
        """
        Set the position of the piece.

        :param x: X coordinate.
        :param y: Y coordinate.
        """
        self.__position = (x, y)

    def set_rotation(self, rotation: int) -> None:
        """
        Set the rotation of the piece.

        :param rotation: Rotation of the piece.
        """
        self.__rotation = rotation

    def get_positions(self) -> t.List[t.Tuple[int, int]]:
        """
        Get the absolute positions of the piece.

        :return: A list of (x, y) tuples.
        """

        board: t.List[t.Tuple[int, int]] = []

        if self.__rotation % 4 == 0:
            board = [(x + self.__position[0], y + self.__position[1])
                     for x, y in self.__relative_positions]
        elif self.__rotation % 4 == 1:
            board = [(y + self.__position[0], -x + self.__position[1])
                     for x, y in self.__relative_positions]
        elif self.__rotation % 4 == 2:
            board = [(-x + self.__position[0], -y + self.__position[1])
                     for x, y in self.__relative_positions]
        elif self.__rotation % 4 == 3:
            board = [(-y + self.__position[0], x + self.__position[1])
                     for x, y in self.__relative_positions]

        # if any of the positions are out of bounds, return an empty list
        if any(x < 0 or x >= 6 or y < 0 or y >= 6 for x, y in board):
            return []
        return board

    def get_color(self) -> str:
        """
        Get the color of the piece.

        :return: The color of the piece.
        """
        return self.__color
