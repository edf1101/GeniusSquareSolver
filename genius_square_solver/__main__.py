"""
This is the main code file for the Genius Square Solver.
"""

import typing as t
from random import choice
from colorama import Fore, Style
from piece import Piece


class App:
    """
    This is the main application class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.pieces = self.__create_pieces()
        self.blocks = self.__create_blocks()



    def __create_pieces(self) -> t.List[Piece]:
        """
        Create the pieces.

        :return: A list of pieces.
        """

        # can find a table of ANSI colours here we are using 256 set https://github.com/fidian/ansi
        piece_1 = Piece("\u001b[38;5;21m", [(0, 0)])
        piece_2 = Piece("\u001b[38;5;52m", [(0, 0), (1, 0)])
        piece_3 = Piece("\u001b[38;5;208m", [(0, 0), (1, 0), (2, 0)])
        piece_4 = Piece("\u001b[38;5;248m", [(0, 0), (1, 0), (2, 0), (3, 0)])
        piece_2x2 = Piece("\u001b[38;5;22m", [(0, 0), (1, 0), (0, 1), (1, 1)])
        piece_90deg = Piece("\u001b[38;5;54m", [(0, 0), (1, 0), (1, 1)])
        piece_l = Piece("\u001b[38;5;45m", [(0, 0), (1, 0), (2, 0), (2, 1)])
        piece_t = Piece("\u001b[38;5;11m", [(0, 0), (1, 0), (2, 0), (1, 1)])
        piece_s = Piece("\u001b[38;5;1m", [(0, 0), (1, 0), (1, 1), (2, 1)])

        return [piece_1, piece_2, piece_3, piece_4, piece_2x2, piece_90deg, piece_l, piece_t,
                piece_s]

    def __letter_coord_to_index(self, letter: str) -> tuple[int, int]:
        """
        Convert a letter coordinate to an index.

        :param letter: The letter coordinate.
        :return: The index.
        """
        letter = letter.upper().strip()
        return int(letter[1]) - 1, ord(letter[0]) - ord('A')

    def __create_blocks(self) -> t.List[t.Tuple[int, int]]:
        """
        Create the blocks.

        :return: The list of blocks as (x, y) tuples.
        """

        all_dice = ['E6,F5,E4,F4,D5,E5', 'F3,D2,E2,C1,A1,D1', 'F1,F1,A6,F1,A6,A6',
                    'B1,C2,A2,B3,A3,B2',
                    'A5,E1,A5,B6,F2,F2', 'C4,D3,B4,C3,D4,E3', 'C5,F6,A4,D6,C6,B5']

        return [self.__letter_coord_to_index(choice(die.split(','))) for die in all_dice]

    def print_board(self, markers: t.List[t.Tuple[int, int]],
                      pieces: t.List[t.Tuple[str, t.List[t.Tuple[int, int]]]]) -> None:
        """
        Print the board with the given markers and pieces.

        :param markers: A list of (x, y) tuples for the markers.
        :param pieces: A list of (piece, (x, y)) tuples for the pieces.
        :return:
        """
        marker_col = "\u001b[38;5;94m"

        for y in range(6):
            for x in range(6):

                print(Style.RESET_ALL + Fore.RESET, end='')
                if (x, y) in markers:
                    print(marker_col + ' ● ', end='')
                else:
                    col = None
                    for color, positions in pieces:
                        # Check if the current position is in the piece.
                        if (x, y) in positions:
                            col = color
                            break

                    if col is not None:
                        print(col + " ■ ", end='')
                    else:
                        print(Fore.WHITE + ' X ', end='')
            print()

    def solve(self) -> bool:
        """
        Solve the puzzle.

        :return: True if solved in good time. False otherwise.
        """

        return False


if __name__ == '__main__':
    main_app = App()
    main_app.solve()
