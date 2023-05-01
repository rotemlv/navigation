import heapdict


class Node:
    def __init__(self, path_cost_ceiling=float('inf')):
        """Create a node for navigation"""
        self.heuristic = lambda x: 0
        self.path_cost_ceiling = path_cost_ceiling

    def get_neighbors(self):
        """Get the neighbors of the calling object"""
        pass

    def get_neighbors_with_cost(self):
        """Get a list of tuples: (neighbor, cost) for each neighbor of the calling object"""
        pass

    @staticmethod
    def __reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return list(reversed(total_path))

    def to_string(self):
        return f"{self.__class__}.{self}"

    def __a_star(self, goal, h, max_path_cost):
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        heap = heapdict.heapdict()
        # For node n, came_from[n] is the node immediately preceding it on the cheapest path from the start
        # to n currently known.
        came_from = {}

        # For node n, g_score[n] is the cost of the cheapest path from start to n currently known.
        g_score = {self: 0}

        # For node n, f_score[n] := g_score[n] + h(n). f_score[n] represents our current best guess as to
        # how cheap a path could be from start to finish if it goes through n.
        f_score = {self: h(self)}
        heap[self] = f_score[self]
        closed = set()
        while len(heap):
            # This operation can occur in O(Log(N)) time if heap is a min-heap or a priority queue
            # current = the node in heap having the lowest f_score[] value
            current, cost = heap.popitem()
            closed.add(current)
            if current == goal:
                print(f"Total nodes looked at: {len(closed) + len(heap)}")
                return self.__reconstruct_path(came_from, current)

            for b_neighbor, cost in current.get_neighbors_with_cost():
                # The following branch is not a part of original pseudocode, requires testing!
                if b_neighbor in closed:
                    continue
                tentative_g_score = g_score[current] + cost  # 1 is always the distance for us
                if tentative_g_score < g_score.setdefault(b_neighbor, max_path_cost + 1):
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[b_neighbor] = current
                    g_score[b_neighbor] = tentative_g_score
                    f_score[b_neighbor] = tentative_g_score + h(b_neighbor)
                    heap[b_neighbor] = f_score[b_neighbor]

        # Open set is empty but goal was never reached (returns None)

    def _search(self, goal, heuristic=None):
        """Implementation of A star - traverse from current object to a given target.
        :param goal: Must be of the same type as the calling object for comparison's sake
        :param heuristic: Either assigned here, at the constructor, or using self.set_heuristic().
                          If heuristic is undefined, algorithm uses lambda x: 0
        """
        if heuristic is not None:
            current_heuristic = heuristic
        else:
            current_heuristic = self.heuristic
        return self.__a_star(goal, current_heuristic, self.path_cost_ceiling)
