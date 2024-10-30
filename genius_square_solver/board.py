"""
This module contains the board class.
"""

import typing as t
from copy import deepcopy
from time import time
import numpy as np
from piece import Piece
from colorama import Fore, Style


class Board:
    """
    This board class represents the game board.
    """

    def __init__(self, blockers: t.List[t.Any], limit: int = 10, time_limit:int=20) -> None:
        """
        Constructor to set up the board.

        :param blockers: A list of the blocker positions to use.
        :param limit: The maximum number of solutions to find.
        :return: None
        """

        self.__start_solve = 0
        self.__blockers = blockers
        self.__pieces = self.__create_pieces()
        self.__solutions: list[Board] = []
        self.__limit = limit
        self.__time_limit = time_limit

        self.__space = np.zeros((6, 6), np.int8)

        for blocker in self.__blockers:
            self.place_piece(blocker[0], blocker[1], self.__pieces[0], 0)

    def get_out_of_time(self) -> bool:
        """
        Get whether the solver has run out of time or not

        :return: The time limit for the solver.
        """

        return time() - self.__start_solve > self.__time_limit

    def get_solution_limit(self) -> int:
        """
        Get the solution limit for the solver.

        :return: The solution limit for the solver.
        """

        return self.__limit

    def add_solution(self, board: t.Self) -> None:
        """
        Add a solution to the board.

        :param board: The board to add.
        :return: None
        """

        self.__solutions.append(board)

    def solve(self) -> bool:
        """
        Solve the board.

        :return: True if the board is solved, False if not.
        """
        self.__start_solve = time()
        self.recursive_solve(self, self.__pieces[1:])

        # if we have solutions, set the board to the first solution's board
        if len(self.__solutions) > 0:
            self.__space = self.__solutions[0].get_space()

        return len(self.__solutions) > 0

    def get_space(self) -> np.ndarray:
        """
        Get the space for the board. This is deepcopied to prevent modification.

        :return: The space for the board.
        """

        return deepcopy(self.__space)

    def get_solutions(self) -> list[t.Self]:
        """
        Get the solutions for the board.

        :return: The solutions for the board.
        """

        return self.__solutions

    def place_piece(self, row: int, col: int, piece: Piece, orientation: int = 0) -> None:
        """
        Place a piece on the board.

        :param row: The row to place the piece.
        :param col: The column to place the piece.
        :param piece: The piece to place.
        :param orientation: The orientation of the piece. 0-3.
        :return: None
        """
        piece_mask = piece.get_masks()[orientation]
        piece_rows, piece_cols = piece_mask.shape
        board_slice = self.__space[row:row + piece_rows, col:col + piece_cols]
        add_slice = piece_mask * piece.get_uuid()
        board_slice[:] += add_slice  # replace the range

    def piece_fits_at_space(self, row: int, col: int, piece: Piece):
        """
        Checks if a Piece can fit on the Board at the given row & column,
        by iterating through each of the piece's orientation masks. The top-
        left of the piece mask will be used as the origin.

        :param row: The row to check.
        :param col: The column to check.
        :param piece: The piece to check.
        :return: index to the GamePiece's mask for the first orientation that will fit on the
         Board. If none fit, return None.
        """

        for mask_index, piece_mask in enumerate(piece.get_masks()):
            piece_rows, piece_cols = piece_mask.shape

            # Get the slice of the board where the piece will be placed
            board_slice = self.__space[row:row + piece_rows, col:col + piece_cols]

            if board_slice.shape != piece_mask.shape:
                # the size of the resulting board slice and the size of the
                # piece don't match up, which means the piece extended past the
                # edge of the board.
                continue

            # If bitwise AND operation of empty spaces & piece mask equals the piece mask, it fits.
            if np.array_equal((board_slice == 0) & piece_mask, piece_mask):
                return mask_index

        return None  # does not fit

    def __str__(self) -> str:
        """
        String representation of the board.

        :return: Return a string representation of the board
        """

        return_string = ''
        for y in range(6):
            for x in range(6):

                return_string += (Style.RESET_ALL + Fore.RESET)

                uuid = self.__space[x, y]
                if uuid == 0:
                    col = None
                else:
                    col = self.__get_piece_text_colour_by_id(uuid)

                if col is not None:
                    if uuid == self.__pieces[0].get_uuid():
                        return_string += (col + ' ● ')
                    else:
                        return_string += (col + " ■ ")
                else:
                    return_string += (Fore.WHITE + ' X ')
            return_string += '\n' + Fore.RESET + Style.RESET_ALL
        return return_string

    def __get_piece_text_colour_by_id(self, uuid):
        """
        Get the text colour for a piece by its ID.

        :param uuid: The ID of the piece.
        :return: The text colour.
        """
        found_id = 0
        for piece in self.__pieces:
            if piece.get_uuid() == uuid:
                found_id = piece
                break
        return found_id.get_color()

    @staticmethod
    def __create_pieces() -> t.List[Piece]:
        """
        Create the pieces for the board.

        :return: The list of pieces to use.
        """

        blocker = Piece(1,'Blocker',
                            "\u001b[38;5;94m", [0.6, 0.4, 0.05],
                            [[True]])
        blue = (Piece(2,'Blue',
                            "\u001b[38;5;21m", [0, 0, 1.0],
                            [[True]]))
        brown = (Piece(3,'Brown',
                            "\u001b[38;5;52m", [0.5, 0.3, 0.3],
                            [[True, True]]))
        orange = (Piece(4,'Orange',
                            "\u001b[38;5;208m", [1.0, 0.4, 0],
                            [[True, True, True]]))
        grey = (Piece(5,'Grey',
                            "\u001b[38;5;248m", [0.5, 0.5, 0.5],
                            [[True, True, True, True]]))
        red =(Piece(6,'Red',
                            "\u001b[38;5;1m", [1.0, 0, 0],
                            [[False, True, True], [True, True, False]]))
        yellow = (Piece(7,'Yellow',
                            "\u001b[38;5;11m", [1.0, 0.7, 0],
                            [[True, True, True],
                             [False, True, False]]))
        cyan = (Piece(8,'Cyan',
                            "\u001b[38;5;45m", [0.2, 0.5, 1.0],
                            [[True, True, True], [True, False, False]]))
        green = (Piece(9,'Green',
                            "\u001b[38;5;22m", [0, 1.0, 0],
                            [[True, True], [True, True]]))
        purple = (Piece(10,'Purple',
                            "\u001b[38;5;54m", [0.5, 0, 0.5],
                            [[True, True], [True, False]]))

#  pieces = {Blocker,Grey,Red,Yellow,Cyan,Orange,Green,Purple,Brown,Blue};
#         pieces = [blocker, blue, brown, orange, grey, red, yellow, cyan, green, purple]
        pieces = [blocker,grey,red,yellow,cyan,orange,green,purple,brown,blue]

        return pieces

    def is_solved(self) -> bool:
        """
        Gets whether the board is solved or not (any squares  unfilled).

        :return: Boolean value for if its solved.
        """

        return 0 not in self.__space

    def recursive_solve(self, root_board: t.Self, remaining: t.List[Piece]) -> bool:
        """
        Recursive function to solve the puzzle and adds solutions to self.__solutions list.

        :param root_board: The original board object, to add solutions to.
        :param remaining: List of pieces available to place.
        :return: True if a solution was found or max solutions found, False if no solution found.
        """

        piece = remaining[0]  # The piece to try and fit in

        # If we have been solving for more than 20 seconds, return False
        if root_board.get_out_of_time():
            return False

        # Go through all rows and columns to see if we can fit this piece in
        for row in range(6):
            for col in range(6):

                # Get the index orientation of the piece that fits. Or None if it doesn't fit
                orientation = self.piece_fits_at_space(row, col, piece)

                if orientation is not None:
                    # Create a new board with the piece placed so it doesn't affect other
                    # recursive instances.
                    new_board = deepcopy(self)
                    new_board.place_piece(row, col, piece, orientation)
                    new_remaining = remaining.copy()
                    new_remaining.remove(piece)

                    if new_board.is_solved():
                        # If the board is solved, add it to the root board's solutions list.
                        root_board.add_solution(new_board)
                        # If we have found 10 solutions, return True to exit out of the recursion.
                        return len(root_board.get_solutions()) >= root_board.get_solution_limit()

                    # We still have pieces to place, so recursively call this function again.
                    hit_limit = new_board.recursive_solve(root_board, new_remaining)

                    if hit_limit:  # Limit reached in a deeper call
                        return True  # exit out of the recursion

        return False  # No possible solutions with this current recursive state.
