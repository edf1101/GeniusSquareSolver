"""
This is the main code file for the Genius Square Solver.
"""

import typing as t
from dice import letter_coord_to_index
from board import Board
from image_processor import ImageReader


def main() -> None:
    """
    The main function to run a demo solve of Genius Square.

    :return: None
    """

    # Read the image
    print("Reading image...")
    path = '../res/test_board.jpg'
    image_reader = ImageReader(path)
    image_reader.process()

    # create blockers
    blockers = image_reader.get_marker_names()
    blockers: t.List[t.Any] = [letter_coord_to_index(die) for die in blockers]

    # create board
    board = Board(blockers, limit=1)
    print("Read the board as:")
    print(board)

    # Solve it
    print("Solving...")
    board.solve()
    print("Solution:")
    print(board)


if __name__ == '__main__':
    main()
