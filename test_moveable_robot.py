import sys

from ColoredMaze import ColoredMaze
from FilteringMazePredictor import FilteringMazePredictor
import random

maze_file_loc = "./mazes/maze1"
colored_maze = ColoredMaze(maze_file_loc)
Filterer = FilteringMazePredictor(colored_maze)

# Put the robot in a random location in the maze
colored_maze.randomize_robot_location()

# We want to give the option for the robot to know which direction it moved in
robot_knows_decision = ""
robot_knows = False
print("The robot knowing which moves it makes will make its predictions more accurate. If it doesn't know, "
      "it will only rely on color sensor data.")
while robot_knows_decision != "y" and robot_knows_decision != "n":
    robot_knows_decision = input("Should the robot know what moves it makes? Enter 'y' or 'n'\n")

if robot_knows_decision == "y":
    robot_knows = True

directions = []
sensor_readings = []
valid_moves = {'N', 'E', 'S', 'W'}
direction = input("Enter move from {N, E, S, W} (lowercase allowed) or 'm' to show the current maze and robot:\n")
direction = direction.upper()
direction = direction.strip()
while direction:
    if direction in valid_moves:
        # Make the move
        directions.append(direction)
        colored_maze.attempt_robot_move(direction)
        # Sense the color
        color_sensed = colored_maze.get_color_faulty(colored_maze.robot_loc[0], colored_maze.robot_loc[1])
        sensor_readings.append(color_sensed)
        print(f"Attempted to move {direction} and sensed color {color_sensed}")

        # Calculate the probability distribution
        if robot_knows:
            prob_dist = Filterer.solve_for_probability_distribution(sensor_readings, directions)
        else:
            prob_dist = Filterer.solve_for_probability_distribution(sensor_readings)

        # Show where we might be:
        colored_maze.illustrate_probabilities(prob_dist)
    elif direction == "M":
        print(colored_maze)
    else:
        print("Invalid input", file=sys.stderr)
    direction = input("Enter move here from {N, E, S, W} (lowercase accepted): ").upper()
    direction = direction.strip()


