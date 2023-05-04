import copy
import random
from Node import Node
from console_colors import Bcolors

PATH_B_COLOR = Bcolors.OKGREEN


class Maze(Node):
    """
    Maze is ALSO built as an example for how to "implement" the Node "interface".\n ...
    """

    def __init__(self, start_state, goal_state, width, height, food_locations=None, _conditions_with_moves=None):
        assert len(start_state) == len(goal_state)
        super().__init__()
        self.state = start_state
        self.goal = goal_state
        self.width = width
        self.height = height
        if food_locations is not None:
            self.food_locations = food_locations
        else:
            self.food_locations = []
            for i in range(len(self.state)):
                if self.state[i] == 'F':
                    self.food_locations.append(i)
        if _conditions_with_moves is None:
            # in a true "OOP" version this would be an enum or a constant field for this class
            # even more so, it would be a hashmap where these would be values, with keys like UP,DOWN
            self._conditions_with_moves = [(lambda x: x % self.width > 0, -1),
                                           (lambda x: x % self.width < (self.width - 1), 1),
                                           (lambda x: x > (self.width - 1), - self.width),
                                           (lambda x: x < self.width * (self.height - 1), self.width)]
        else:
            self._conditions_with_moves = _conditions_with_moves

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(' '.join(map(str, self.state)))

    def __repr__(self):
        _s = ""
        for i, elem in enumerate(self.state):
            _s += elem
            if i % self.width == self.width - 1:
                _s += '\n'
        return _s

    def to_string(self):
        return ''.join(map(str, self.state))

    def get_neighbors_with_cost_(self):
        # possible swaps stores new states after the swap
        possible_swaps = []
        try:
            # where is our maze's traveler:
            z = self.state.index('S')
            # left possible?
            if z % self.width > 0:
                self._get_possible_move(possible_swaps, z, z - 1)
            # right possible?
            if z % self.width < (self.width - 1):
                self._get_possible_move(possible_swaps, z, z + 1)
            # up possible?
            if z > self.width - 1:
                self._get_possible_move(possible_swaps, z, z - self.width)
            if z < self.width * (self.height - 1):
                self._get_possible_move(possible_swaps, z, z + self.width)
        except ValueError:
            pass
        if not possible_swaps:
            print(f"No moves possible in current state (\n{self})\n")
        return possible_swaps

    def get_neighbors_with_cost(self):
        # possible swaps stores new states after the swap
        possible_swaps = []
        try:
            # where is our maze's traveler:
            z = self.state.index('S')
            for cond, move in self._conditions_with_moves:
                move += z
                if cond(z):
                    self._get_possible_move(possible_swaps, z, move)
        except ValueError:
            pass
        if not possible_swaps:
            print(f"No moves possible in current state (\n{self})\n")
        return possible_swaps

    def _get_possible_move(self, possible_swaps, curr_pos, new_pos):
        if self.state[new_pos] != '#':
            ls = self.state.copy()
            ls[curr_pos], ls[new_pos] = ls[new_pos], ls[curr_pos]
            if ls[curr_pos] == 'F':
                ls[curr_pos] = '.'
                if 'F' not in ls:
                    ls[new_pos] = '.'
            possible_swaps.append((Maze(ls, self.goal, self.width, self.height,
                                        _conditions_with_moves=self._conditions_with_moves), 1))

    def scramble(self, how_long):
        for _ in range(how_long):
            neighbors = self.get_neighbors_with_cost()
            self.state = neighbors[random.randint(0, len(neighbors) - 1)][0].state

    def search(self, heuristic=None):
        return super()._search(Maze(self.goal, self.goal, self.width, self.height,
                                    self._conditions_with_moves), heuristic)


def print_path(path: list, maze_height: int, maze_width: int, width: int):
    i = 0
    while i < len(path):
        # print all first lines in current width
        boards = path[i: i + width]
        for j in range(maze_height):
            for board in boards:
                # print current row
                print(board.state[maze_width * j: maze_width * j + maze_width],
                      end='    ' if j != 1 or board.state == board.goal else ' -> ')
            print()
        print()
        i += width


def print_path_colorful_show_change_on_prev_board(path: list, maze_height: int, maze_width: int, width: int):
    i = 0
    last_board = None
    path = path + [path[-1]]
    start_board = path[0]
    while i < len(path):
        # print all first lines in current width
        boards = path[i: i + width + int(i == 0)]
        for j in range(maze_height):
            for m, board in enumerate(boards):
                if i and not m:
                    last_board = path[i - 1]
                if not i and not m:
                    last_board = path[0]
                    continue
                # print current row
                curr_idx = m + i
                if board != start_board and (tmp := last_board.state[maze_width * j: maze_width * j + maze_width]) != (
                        curr := board.state[maze_width * j: maze_width * j + maze_width]):
                    # print the difference in red
                    print(f"", end='')
                    for k, (elem, old_elem) in enumerate(zip(curr, tmp)):
                        print(f"{elem}", sep='', end='') if elem == old_elem else \
                            print(f"{PATH_B_COLOR}{old_elem}{Bcolors.ENDC}", sep='', end='')
                        if k == maze_width - 1:
                            print("", end='    ' if j != 1 or last_board.state == board.state else ' -> ')
                else:
                    print(''.join(board.state[maze_width * j:maze_width * j + maze_width]),
                          end='    ' if j != 1 or last_board.state == board.goal else ' -> ')
                last_board = path[curr_idx]
            print()
        print()
        i += width


def print_path_colorful_prev_as_lists(path: list, maze_height: int, maze_width: int, width: int):
    """Shows the maze inside lists, unwieldy for larger mazes"""
    i = 0
    last_board = None
    path = path + [path[-1]]
    start_board = path[0]
    while i < len(path):
        # print all first lines in current width
        boards = path[i: i + width + int(i == 0)]
        for j in range(maze_height):
            for m, board in enumerate(boards):
                if i and not m:
                    last_board = path[i - 1]
                if not i and not m:
                    last_board = path[0]
                    continue
                # print current row
                curr_idx = m + i
                if board != start_board and (tmp := last_board.state[maze_width * j: maze_width * j + maze_width]) != (
                        curr := board.state[maze_width * j: maze_width * j + maze_width]):
                    # print the difference in red
                    print(f"[", end='')
                    for k, (elem, old_elem) in enumerate(zip(curr, tmp)):
                        print(f"\'{elem}\'", sep='', end='') if elem == old_elem else \
                            print(f"{PATH_B_COLOR}\'{old_elem}\'{Bcolors.ENDC}", sep='', end='')
                        if k < maze_width - 1:
                            print(f', ', sep='', end='')
                        else:
                            print("]", end='    ' if j != 1 or last_board.state == board.state else ' -> ')
                else:
                    print(board.state[maze_width * j:maze_width * j + maze_width],
                          end='    ' if j != 1 or last_board.state == board.goal else ' -> ')
                last_board = path[curr_idx]
            print()
        print()
        i += width


maze = [
    '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.', '#', '.', '.',
    '.', '.', '.', '.', '.', '#', '#', '.', 'F', '.', '#', '.', '.', '.', '.',
    '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '#', '#', '.', '.', '.',
    '.', '#', '#', '.', '.', '.', '.', '.', '#', '#', 'F', '#', '#', '.', '.',
    '.', '.', '#', '#', 'F', '#', '#', '.', '.', '.', '.', '.', '#', '.', '.',
    '.', '.', '.', '#', '#', '#', 'F', '.', '#', '.', '.', '.', '#', '#', '.',
    '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.',
    'S', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.',
]

jolly = [
    '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.', '#', '.', '.',
    '.', '.', '.', '.', '.', '#', '#', '.', '.', '.', '#', '.', '.', '.', '.',
    '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '#', '#', '.', '.', '.',
    '.', '#', '#', '.', '.', '.', '.', '.', '#', '#', '.', '#', '#', '.', '.',
    '.', '.', '#', '#', '.', '#', '#', '.', '.', '.', '.', '.', '#', '.', '.',
    '.', '.', '.', '#', '#', '#', '.', '.', '#', '.', '.', '.', '#', '#', '.',
    '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.',
]

maze = [
    'F', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.', '.', '.', 'F',
    '.', '.', '.', '.', '.', '#', '#', '.', '.', '.', '#', '.', '.', '#', '.',
    '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '#', '#', '.', '#', '.',
    '.', '#', '#', '.', '.', '.', '.', '.', '#', '#', '.', '#', '#', '#', '.',
    '.', '.', '#', '#', '.', '#', '#', '.', '.', '.', '.', '.', '#', '#', '.',
    '.', '.', '.', '#', '#', '#', '.', '.', '#', '.', '.', '.', '#', '#', '.',
    '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.',
    'S', '.', '.', '.', '#', 'F', '.', '.', '.', '#', '.', '.', '.', '.', 'F',
]

jolly = [
    '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '#', '#', '.', '.', '.', '#', '.', '.', '#', '.',
    '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '#', '#', '.', '#', '.',
    '.', '#', '#', '.', '.', '.', '.', '.', '#', '#', '.', '#', '#', '#', '.',
    '.', '.', '#', '#', '.', '#', '#', '.', '.', '.', '.', '.', '#', '#', '.',
    '.', '.', '.', '#', '#', '#', '.', '.', '#', '.', '.', '.', '#', '#', '.',
    '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.',
    '.', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.',
]


def inadmissible_heuristic(maze: Maze):
    try:
        s_location = maze.state.index('S')
        s_row, s_col = s_location // maze.width, s_location % maze.width
        # find distances between S and all foods:
        dists = []
        for food_idx in maze.food_locations:
            f_row, f_col = food_idx // maze.width, food_idx % maze.width
            dists.append(abs(f_row - s_row) + abs(f_col - s_col))
        # sort the dists by the manhattan distance
        return sum(dists)
    except ValueError:
        return 0


def best_heuristic(maze: Maze):
    """Cannot be beaten yet, not for a lack of trying. This heuristic is based on the concept of splitting
    the optimal solution into optimal sub-solutions. (Might have some erroneous edge cases)"""
    try:
        s_location = maze.state.index('S')
        s_row, s_col = s_location // maze.width, s_location % maze.width
        # find distances between S and all foods:
        dists = []
        for food_idx in maze.food_locations:
            f_row, f_col = food_idx // maze.width, food_idx % maze.width
            dists.append(((f_row, f_col), abs(f_row - s_row) + abs(f_col - s_col)))
        # sort the dists by the manhattan distance
        dists.sort(key=lambda x: x[1])
        # take distance from rat to the closest food
        heuristic_sum = dists[0][1]
        # tak distance from each food to the next food, visa vi distance from rat
        for i in range(len(dists) - 1):
            curr, nxt = dists[i], dists[i + 1]
            curr_row, curr_col = curr[0]
            nxt_row, nxt_col = nxt[0]
            # add it
            heuristic_sum += abs(curr_row - nxt_row) + abs(curr_col - nxt_col)
        # etcetra
        return heuristic_sum
    except ValueError:
        return 0


def too_smart_for_its_own_good_heuristic(maze: Maze):
    try:
        s_location = maze.state.index('S')
        s_row, s_col = s_location // maze.width, s_location % maze.width
        # find distances between S and all foods:
        dists = []
        for food_idx in maze.food_locations:
            f_row, f_col = food_idx // maze.width, food_idx % maze.width
            dists.append(((f_row, f_col), abs(f_row - s_row) + abs(f_col - s_col)))
        # sort the dists by the manhattan distance
        dists.sort(key=lambda x: x[1])
        # take distance from rat to the closest food
        heuristic_sum = 0.6 * dists[0][1]
        damnson = 0
        # tak distance from each food to the next food, visa vi distance from rat
        for i in range(len(dists) - 1):
            curr, nxt = dists[i], dists[i + 1]
            curr_row, curr_col = curr[0]
            nxt_row, nxt_col = nxt[0]
            # add it
            damnson += abs(curr_row - nxt_row) + abs(curr_col - nxt_col)
        # etcetra
        return heuristic_sum + 0.4 * damnson
    except ValueError:
        return 0


def min_manhattan_dist_plus_current_num_of_peirot_heuristic(maze: Maze):
    try:
        s_location = maze.state.index('S')
        s_row, s_col = s_location // maze.width, s_location % maze.width
        # find distances between S and all foods:
        dists = []
        for food_idx in maze.food_locations:
            f_row, f_col = food_idx // maze.width, food_idx % maze.width
            dists.append(((f_row, f_col), abs(f_row - s_row) + abs(f_col - s_col)))
        # sort the dists by the manhattan distance
        dists.sort(key=lambda x: x[1])
        # take distance from rat to the closest food
        heuristic_sum = dists[0][1]
        return heuristic_sum + len(maze.food_locations)
    except ValueError:
        return 0


def my_simple_heuristic(maze: Maze):
    try:
        max_dist = -float('inf')
        s_location = maze.state.index('S')
        s_row, s_col = s_location // maze.width, s_location % maze.width
        for idx in maze.food_locations:
            f_row, f_col = idx // maze.width, idx % maze.width
            if (tmp := (abs(f_row - s_row) + abs(f_col - s_col))) > max_dist:
                max_dist = tmp
        return max_dist
    except ValueError:
        return 0


def my_even_simpler_heuristic(maze: Maze):
    count = 0
    for i in range(len(maze.state)):
        if maze.state[i] != maze.goal[i]:
            count += 1
    return count


def generate_maze(width, height, food_count=10, wall_count=10, start_pos=None):
    maze_gen = []
    food_locations = []
    for i in range(width * height):
        maze_gen.append('.')
    # set start position
    if start_pos is None:
        # set at the bottom left
        maze_gen[height * width - width] = 'S'
    for i in range(wall_count):
        while maze_gen[(w := random.randint(0, width * height - 1))] != '.':
            pass
        maze_gen[w] = '#'
    # default goal is eatin' all the food
    goal = copy.deepcopy(maze_gen)
    goal[maze_gen.index('S')] = '.'
    for i in range(food_count):
        while maze_gen[(f := random.randint(0, width * height - 1))] != '.':
            pass
        maze_gen[f] = 'F'
        food_locations.append(f)
    return Maze(maze_gen, goal, width, height, food_locations)


mz = Maze(maze, jolly, 15, 8)
rez = mz.search(best_heuristic)
# rez = mz.search()
# if you use me prepare for a wall of text
# print_path_colorful_show_change_on_prev_board(rez, mz.height, mz.width, 2)
print("Path cost (+1 added since we count nodes not \"hedges\")", len(rez))

m = generate_maze(80, 10, 20, 50)
# g = Maze(m.goal, m.goal, 80, 10)
# print(g)
res = m.search(best_heuristic)
if res:
    print_path_colorful_show_change_on_prev_board(res, m.height, m.width, 2)
else:
    print(F"This maze is not solvable")
