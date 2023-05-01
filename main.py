from time import perf_counter
from EightPuzzle import *


if __name__ == '__main__':
    # a = EightPuzzle([1, 2, 3, 4, 5, 6, 7, 8, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8])
    # ex:
    a = EightPuzzle([7, 4, 3, 6, 5, 1, 2, 8, 0], [1, 2, 3, 4, 5, 6, 7, 8, 0])
    # a = EightPuzzle([7, 4, 3, 6, 5, 1, 2, 8, 0], [1, 2, 3, 4, 5, 6, 7, 8, 0])
    a.scramble(150)
    print("Solve for:\n", a, sep='')
    tmp = perf_counter()
    res = a.search(manhattan_heuristic)
    time_cost = perf_counter() - tmp
    print(len(res))
    print(f"Search took {time_cost} secs\npath:")
    print_path_colorful_show_change_on_prev_board(res, width=12)
