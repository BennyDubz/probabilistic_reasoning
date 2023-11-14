from ColoredMaze import ColoredMaze
from FilteringMazePredictor import FilteringMazePredictor
# Author: Ben Williams '25
# Date: October 31st, 2023

# This maze has a higher weight towards green spaces
maze8x8 = ColoredMaze("./mazes/maze8x8")
Fil_8x8 = FilteringMazePredictor(maze8x8)
path_1_8x8 = ["g", "g", "r", "y", "b", "b", "b", "b"]
path_2_8x8 = ["g", "g", "g", "g", "g", "g", "g", "g"]
sol_1_8x8 = Fil_8x8.solve_for_probability_distribution(path_1_8x8)
sol_2_8x8 = Fil_8x8.solve_for_probability_distribution(path_2_8x8)
print("8x8 Probability Distribution for path 1:")
Fil_8x8.colored_maze.illustrate_probabilities(sol_1_8x8)
print("8x8 Probability Distribution for path 2:")
Fil_8x8.colored_maze.illustrate_probabilities(sol_2_8x8)


