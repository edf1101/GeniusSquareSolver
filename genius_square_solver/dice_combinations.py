"""
This class is used to easily get a die combination for the Genius Square game.
"""

from dice import letter_coord_to_index


class DiceCombo:
    """
    This class is used to easily get a dice combination for the Genius Square game.
    """

    all_dice_faces = ['E6,F5,E4,F4,D5,E5'.split(','),
                      'F3,D2,E2,C1,A1,D1'.split(','),
                      'F1,F1,A6,F1,A6,A6'.split(','),
                      'B1,C2,A2,B3,A3,B2'.split(','),
                      'A5,E1,A5,B6,F2,F2'.split(','),
                      'C4,D3,B4,C3,D4,E3'.split(','),
                      'C5,F6,A4,D6,C6,B5'.split(',')]

    def __init__(self) -> None:
        """
        Constructor to set up the dice combination.
        """

        # Nothing here all is static

    @staticmethod
    def get_blockers(x: int) -> list[tuple[int, int]]:
        """
        Get the blockers for the game.

        :param x: The seed for the blockers.
        :return: The blockers for the game.
        """

        index = DiceCombo.f(x)
        base6 = DiceCombo.to_base_6(index)

        selected_elements = [DiceCombo.all_dice_faces[i][base6[i]] for i in range(7)]

        return [letter_coord_to_index(die) for die in selected_elements]

    @staticmethod
    def f(x) -> int:
        """
        LCG function for mapping x deterministically to a unique integer in [0, 6^7]

        :param x: The input value to map.
        """

        a = 137  # Coprime with 6^7
        c = 17
        n = 6 ** 7

        return (a * x + c) % n

    @staticmethod
    #
    def to_base_6(x:int) -> list[int]:
        """
        Function to convert an integer to a 7-digit base-6 representation

        :param x: The integer to convert.
        :return: The base-6 representation of the integer.
        """
        base6 = []
        for _ in range(7):
            base6.append(x % 6)
            x //= 6
        return base6  # technically reversed but it doesn't matter
