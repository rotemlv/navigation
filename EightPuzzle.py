import random
from Node import Node
from console_colors import Bcolors

PATH_B_COLOR = Bcolors.OKGREEN


class EightPuzzle(Node):
    """
    EightPuzzle is built as an example for how to "implement" the Node "interface".\n
    A class inheriting from Node must implement the __eq__ and __hash__ dunder methods (for maintenance).\n
    Currently, to_string is used for speed testing over different hash functions,
    and its implementation not directly required.\n
    Another required implementation is the get_neighbors_with_cost() method, as this method is used
    by the A* algorithm when the search() method is called. \n
    The final requirement (for ease of use) is the implementation of the search() method,
    this method should simply call: super()._search(self.goal, heuristic)\n
    *Important: when passed to _search, "self.goal" must be of the same type as self itself (lol).*\n
    If you always pass a goal object, you can just implement search() to be an indirect call to _search().\n
    After writing all the aforementioned class methods for your specific use, you can just use obj.search(target, ...),
    and pass (or not) a heuristic function to be used.
    """
    def __init__(self, start_state, goal_state):
        assert len(start_state) == len(goal_state) == 9
        super().__init__(32)
        self.state = start_state
        self.goal = goal_state

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(' '.join(map(str, self.state)))

    def __str__(self):
        sb = ""
        for i in range(3 * 3):
            sb += f"{self.state[i]} "
            if i % 3 == 2:
                sb += "\n"
        return sb

    def to_string(self):
        return ''.join(map(str, self.state))

    def get_neighbors_as_lists(self):
        # possible swaps stores new states after the swap
        possible_swaps = []
        # where is zero:
        z = self.state.index(0)
        # left possible?
        if z % 3 > 0:
            ls = self.state.copy()
            ls[z], ls[z - 1] = ls[z - 1], ls[z]
            possible_swaps.append(ls)
        # right possible?
        if z % 3 < 2:
            rs = self.state.copy()
            rs[z], rs[z + 1] = rs[z + 1], rs[z]
            possible_swaps.append(rs)
        # up possible?
        if z > 2:
            us = self.state.copy()
            us[z], us[z - 3] = us[z - 3], us[z]
            possible_swaps.append(us)
        if z < 6:
            ds = self.state.copy()
            ds[z], ds[z + 3] = ds[z + 3], ds[z]
            possible_swaps.append(ds)
        return possible_swaps

    def get_neighbors_as_lists_with_cost(self):
        # possible swaps stores new states after the swap
        possible_swaps = []
        # where is zero:
        z = self.state.index(0)
        # left possible?
        if z % 3 > 0:
            ls = self.state.copy()
            ls[z], ls[z - 1] = ls[z - 1], ls[z]
            possible_swaps.append((ls, 1))
        # right possible?
        if z % 3 < 2:
            rs = self.state.copy()
            rs[z], rs[z + 1] = rs[z + 1], rs[z]
            possible_swaps.append((rs, 1))
        # up possible?
        if z > 2:
            us = self.state.copy()
            us[z], us[z - 3] = us[z - 3], us[z]
            possible_swaps.append((us, 1))
        if z < 6:
            ds = self.state.copy()
            ds[z], ds[z + 3] = ds[z + 3], ds[z]
            possible_swaps.append((ds, 1))
        return possible_swaps

    def get_neighbors(self):
        # possible swaps stores new states after the swap
        possible_swaps = []
        # where is zero:
        z = self.state.index(0)
        # left possible?
        if z % 3 > 0:
            ls = self.state.copy()
            ls[z], ls[z - 1] = ls[z - 1], ls[z]
            possible_swaps.append(EightPuzzle(ls, self.goal))
        # right possible?
        if z % 3 < 2:
            rs = self.state.copy()
            rs[z], rs[z + 1] = rs[z + 1], rs[z]
            possible_swaps.append(EightPuzzle(rs, self.goal))
        # up possible?
        if z > 2:
            us = self.state.copy()
            us[z], us[z - 3] = us[z - 3], us[z]
            possible_swaps.append(EightPuzzle(us, self.goal))
        if z < 6:
            ds = self.state.copy()
            ds[z], ds[z + 3] = ds[z + 3], ds[z]
            possible_swaps.append(EightPuzzle(ds, self.goal))
        return possible_swaps

    def get_neighbors_with_cost(self):
        # possible swaps stores new states after the swap
        possible_swaps = []
        # where is zero:
        z = self.state.index(0)
        # left possible?
        if z % 3 > 0:
            ls = self.state.copy()
            ls[z], ls[z - 1] = ls[z - 1], ls[z]
            possible_swaps.append((EightPuzzle(ls, self.goal), 1))
        # right possible?
        if z % 3 < 2:
            rs = self.state.copy()
            rs[z], rs[z + 1] = rs[z + 1], rs[z]
            possible_swaps.append((EightPuzzle(rs, self.goal), 1))
        # up possible?
        if z > 2:
            us = self.state.copy()
            us[z], us[z - 3] = us[z - 3], us[z]
            possible_swaps.append((EightPuzzle(us, self.goal), 1))
        if z < 6:
            ds = self.state.copy()
            ds[z], ds[z + 3] = ds[z + 3], ds[z]
            possible_swaps.append((EightPuzzle(ds, self.goal), 1))
        return possible_swaps

    def scramble(self, how_long):
        for _ in range(how_long):
            neighbors = self.get_neighbors_as_lists()
            self.state = neighbors[random.randint(0, len(neighbors) - 1)]

    def search(self, heuristic=None):
        return super()._search(EightPuzzle(self.goal, self.goal), heuristic)


def collision_heuristic(n):
    c = 0
    for i in range(len(n.state)):
        if n.state[i] != n.goal[i]:
            c += 1
    return c


def manhattan_heuristic(n):
    c = 0
    for i, val in enumerate(n.state):
        # what is the value in index i?
        if val:
            # where is this value in the goal?
            j = n.goal.index(val)
            # manhattan:
            r1, c1 = i // 3, i % 3
            r2, c2 = j // 3, j % 3
            c += abs(r1 - r2) + abs(c1 - c2)
    return c


def print_path(path: list, width: int):
    i = 0
    while i < len(path):
        # print all first lines in current width
        boards = path[i: i + width]
        for j in range(3):
            for board in boards:
                # print current row
                print(board.state[3 * j: 3 * j + 3], end='    ' if j != 1 or board.state == board.goal else ' -> ')
            print()
        print()
        i += width


def print_path_colorful(path: list, width: int):
    i = 0
    last_board = None
    start_board = path[0]
    while i < len(path):
        # print all first lines in current width
        boards = path[i: i + width]
        for j in range(3):
            for m, board in enumerate(boards):
                if i and not m:
                    last_board = path[i - 1]
                # print current row
                curr_idx = m + i
                if board != start_board and (tmp := last_board.state[3 * j: 3 * j + 3]) != (
                        curr := board.state[3 * j: 3 * j + 3]):
                    # print the difference in red
                    print(f"[", end='')
                    for k, (elem, old_elem) in enumerate(zip(curr, tmp)):
                        print(f"{elem}", sep='', end='') if elem == old_elem else \
                            print(f"{PATH_B_COLOR}{elem}{Bcolors.ENDC}", sep='', end='')
                        if k < 2:
                            print(', ', sep='', end='')
                        else:
                            print("]", end='    ' if j != 1 or board.state == board.goal else ' -> ')
                else:
                    print(board.state[3 * j: 3 * j + 3], end='    ' if j != 1 or board.state == board.goal else ' -> ')
                last_board = path[curr_idx]
            print()

        print()
        i += width


def print_path_colorful_show_change_on_prev_board(path: list, width: int):
    i = 0
    last_board = None
    path = path + [path[-1]]
    start_board = path[0]
    while i < len(path):
        # print all first lines in current width
        boards = path[i: i + width + int(i == 0)]
        for j in range(3):
            for m, board in enumerate(boards):
                if i and not m:
                    last_board = path[i - 1]
                if not i and not m:
                    last_board = path[0]
                    continue
                # print current row
                curr_idx = m + i
                if board != start_board and (tmp := last_board.state[3 * j: 3 * j + 3]) != (
                        curr := board.state[3 * j: 3 * j + 3]):
                    # print the difference in red
                    print(f"[", end='')
                    for k, (elem, old_elem) in enumerate(zip(curr, tmp)):
                        print(f"{elem}", sep='', end='') if elem == old_elem else \
                            print(f"{PATH_B_COLOR}{old_elem}{Bcolors.ENDC}", sep='', end='')
                        if k < 2:
                            print(', ', sep='', end='')
                        else:
                            print("]", end='    ' if j != 1 or last_board.state == board.goal else ' -> ')
                else:
                    print(board.state[3*j:3*j+3], end='    ' if j != 1 or last_board.state == board.goal else ' -> ')
                last_board = path[curr_idx]
            print()
        print()
        i += width
