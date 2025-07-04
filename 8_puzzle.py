import heapq
class EightPuzzle:
    def __init__(self, start_state):
        """
        Initializes the 8-puzzle problem with a given starting state.

        Parameters:
            start_state (tuple): The initial state of the puzzle, represented as a tuple
                                 of 9 elements where 0 denotes the blank space.
        """
        self.start_state = start_state
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # Goal state of the puzzle

    def is_goal(self, state): # 2 Marks
        """
        Determines if the given state is the goal state of the puzzle.

        Parameters:
            state (tuple): The current state to check against the goal state.

        Returns:
            bool: True if the given state is the goal state, False otherwise.
        """
        return state==self.goal_state ## fix this
    def left(self,state,index):
      state = list(state)
      x=state[index-1]
      state[index-1] = 0
      state[index] = x
      return tuple(state)
    def down(self,state,index):
      state = list(state)
      x=state[index+3]
      state[index+3] = 0
      state[index] = x
      return tuple(state)
    def up(self,state,index):
      state = list(state)
      x=state[index-3]
      state[index-3] = 0
      state[index] = x
      return tuple(state)
    def right(self,state,index):
      state = list(state)
      x=state[index+1]
      state[index+1] = 0
      state[index] = x
      return tuple(state)



    def get_neighbors(self, state): # 8 Marks
        """
        Generates and returns all valid neighboring states from the current state by
        sliding a tile into the blank space.

        Parameters:
            state (tuple): The current state of the puzzle.

        Returns:
            list: A list of tuples, each representing a valid neighboring state after
                  making one move.
        """
        # write your code here
        successor = []
        for i in range(len(state)):
         if state[i] == 0:
            if i == 0:
                new_state = self.right(state, i)
                successor.append(new_state)
                new_state = self.down(state, i)
                successor.append(new_state)
            elif i == 1:
                new_state = self.left(state, i)
                successor.append(new_state)
                new_state = self.right(state, i)
                successor.append(new_state)
                new_state = self.down(state, i)
                successor.append(new_state)
            elif i == 2:
                new_state = self.left(state, i)
                successor.append(new_state)
                new_state = self.down(state, i)
                successor.append(new_state)
            elif i == 3:
                new_state = self.up(state, i)
                successor.append(new_state)
                new_state = self.right(state, i)
                successor.append(new_state)
                new_state = self.down(state, i)
                successor.append(new_state)
            elif i == 4:
                new_state = self.left(state, i)
                successor.append(new_state)
                new_state = self.right(state, i)
                successor.append(new_state)
                new_state = self.up(state, i)
                successor.append(new_state)
                new_state = self.down(state, i)
                successor.append(new_state)
            elif i == 5:
                new_state = self.up(state, i)
                successor.append(new_state)
                new_state = self.left(state, i)
                successor.append(new_state)
                new_state = self.down(state, i)
                successor.append(new_state)
            elif i == 6:
                new_state = self.up(state, i)
                successor.append(new_state)
                new_state = self.right(state, i)
                successor.append(new_state)
            elif i == 7:
                new_state = self.up(state, i)
                successor.append(new_state)
                new_state = self.right(state, i)
                successor.append(new_state)
                new_state = self.left(state, i)
                successor.append(new_state)
        return successor

    def manhattan_distance(self, state): # 10 Marks
        """
        Computes the Manhattan distance heuristic for the 8-puzzle, which is the sum
        of the distances each tile is from its goal position.

        Parameters:
            state (tuple): The current state of the puzzle.

        Returns:
            int: The total Manhattan distance of all tiles from their goal positions.
        """
        distance = 0
        for i in range(9):
            if state[i] == 0:
                continue
            x, y = i % 3, i // 3
            gx, gy = (state[i] - 1) % 3, (state[i] - 1) // 3
            distance += abs(x - gx) + abs(y - gy)
        return distance

    def a_star(self):
        """
        Solves the 8-puzzle using the A* search algorithm with the Manhattan distance heuristic.

        Returns:
            list: A list of states representing the path from the initial state to the
                  goal state, or None if no solution is found.
        """
        # write your code here
        open_list = [(self.manhattan_distance(self.start_state), 0, [self.start_state])]  # (f_cost, g_cost, path)
        closed_list = set()
        g_costs = {self.start_state: 0}

        while open_list:
            f_cost, g_cost, path = heapq.heappop(open_list)
            current_state = path[-1]

            if self.is_goal(current_state):
                return path

            closed_list.add(current_state)
            for neighbor in self.get_neighbors(current_state):
                new_g_cost = g_cost + 1
                if neighbor in closed_list:
                    continue
                if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_g_cost
                    h_cost = self.manhattan_distance(neighbor)
                    f_cost = g_cost + h_cost
                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (f_cost, new_g_cost, new_path))
    def hill_climbing(self, max_iterations=1000):
        """
        Solves the 8-puzzle using Hill Climbing with Manhattan distance.

        Returns:
            list: Path to goal if found, otherwise the local minimum path.
        """
        current = self.start_state
        path = [current]

        for _ in range(max_iterations):
            if self.is_goal(current):
                return path

            neighbors = self.get_neighbors(current)
            neighbors = sorted(neighbors, key=self.manhattan_distance)

            best_neighbor = neighbors[0]
            if self.manhattan_distance(best_neighbor) < self.manhattan_distance(current):
                current = best_neighbor
                path.append(current)
            else:
                break  # Local optimum reached

        return path if self.is_goal(current) else None

# Example usage
initial_state = (2, 8, 3, 1, 6, 4, 7, 0, 5)  # Example of a scrambled puzzle
puzzle = EightPuzzle((1,2,3,0,4,6,7,5,8))
# print(puzzle.is_goal((1, 2, 3, 4, 5, 6, 7, 8, 0)))
solution = puzzle.a_star()


if solution:
    print("Solution Path:")
    for state in solution:
        print(state)
else:
    print("No solution found.")

# Example usage
initial_state = (2, 8, 3, 1, 6, 4, 7, 0, 5)  # Example of a scrambled puzzle
puzzle = EightPuzzle((1,2,3,0,4,6,7,5,8))
# print(puzzle.is_goal((1, 2, 3, 4, 5, 6, 7, 8, 0)))
solution = puzzle.hill_climbing()


if solution:
    print("Solution Path:")
    for state in solution:
        print(state)
else:
    print("No solution found.")
