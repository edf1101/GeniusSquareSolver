"""
This is the code file for the random solver mode for the Genius Square Solver project.
"""

from time import time_ns

from board import Board
from dice_combinations import DiceCombo


def time(seed: int) -> float:
    """
    The function to time solving a seed.

    :param seed: The seed to solve.
    :return: The time taken to solve the seed in nanoseconds.
    """

    # create board
    board = Board(DiceCombo.get_blockers(seed), limit=1, time_limit=600)

    # time it in ns
    start_time = time_ns()
    board.solve()
    end_time = time_ns()

    duration = (end_time - start_time) / 1_000_000_000

    return duration


def main() -> None:
    """
    The main function to run a demo solve of Genius Square.

    :return: None
    """

    count = 0
    _sum = 0

    for seed in range(10000):
        duration = time(seed)
        count += 1
        _sum += duration
        if count % 50 == 0:
            # every 100 times print the count and average in ms
            print(f"Count: {count}, Average: {round((_sum / float(count)) * 1000)}ms")


if __name__ == '__main__':
    main()
