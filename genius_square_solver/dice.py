"""
This module contains the dice class
"""

from random import choice
import typing as t


class Die:
    """
    This class represents a die that can be rolled.
    """

    def __init__(self, options: t.List[t.Any]) -> None:
        """
        Constructor to set up the dice

        :param options: The options that the die can land on
        """

        # error checking
        if not options:
            raise ValueError("Options must not be empty")
        if not isinstance(options, list):
            raise TypeError("Options must be a list")

        self.__options = options

    def throw(self) -> t.Any:
        """
        Throw the die

        :return: The result of the throw
        """

        return choice(self.__options)

    def __str__(self):
        """
        String representation of the die

        :return: The string representation of the die
        """

        descriptions = [str(option) for option in self.__options]

        return f"Die with options: {', '.join(descriptions)}"


def letter_coord_to_index(letter: str) -> tuple[int, int]:
    """
    Convert a letter coordinate to an index.

    :param letter: The letter coordinate.
    :return: The index.
    """
    letter = letter.upper().strip()
    return int(letter[1]) - 1, ord(letter[0]) - ord('A')
