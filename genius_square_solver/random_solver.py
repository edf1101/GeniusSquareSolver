"""
This is the code file for the random solver mode for the Genius Square Solver project.
"""

import typing as t
from dice import Die, letter_coord_to_index
from board import Board


def main() -> None:
    """
    The main function to run a demo solve of Genius Square.

    :return: None
    """
    # create dice
    all_dice_faces = ['E6,F5,E4,F4,D5,E5', 'F3,D2,E2,C1,A1,D1', 'F1,F1,A6,F1,A6,A6',
                      'B1,C2,A2,B3,A3,B2', 'A5,E1,A5,B6,F2,F2', 'C4,D3,B4,C3,D4,E3',
                      'C5,F6,A4,D6,C6,B5']
    dice: t.List[Die] = [Die(dice_face.split(',')) for dice_face in all_dice_faces]
    # create blockers
    blockers = [die.throw() for die in dice]
    blockers: t.List[t.Any] = [letter_coord_to_index(die) for die in blockers]

    # create board
    board = Board(blockers, limit=1)
    print("Solving the random board...")
    print(board)
    board.solve()
    print("Solution to the random board:")
    print(board)


if __name__ == '__main__':
    main()
