import sys

from ColoredMaze import ColoredMaze
import numpy as np

# Author: Ben Williams '25
# Date: October 30th, 2023


# A filtering algorithm for determining the probability of where a robot is in the maze
#   given a sequence of sensor readings.
# Rules:
#   The robot is blind, if it tries to move North and hits a wall, it doesn't know that it failed.
#   The robot has a mostly-working color sensor. If it is over the color blue, the sensor will report "b"
#       88% of the time, red 4% of the time, green 4% of the time, and yellow 4% of the time
class FilteringMazePredictor:
    def __init__(self, colored_maze):
        self.colored_maze = colored_maze

        # Get the initial state of possibilities represented as a 1D array
        self.initial_state = self.get_initial_state()
        self.movement_matrix = self.random_movement_matrix()

        # Get the vectors for how likely it is that we see a color at a given space
        self.color_vectors = dict()
        self.color_vectors["r"] = self.colored_maze.get_color_vector("r")
        self.color_vectors["g"] = self.colored_maze.get_color_vector("g")
        self.color_vectors["b"] = self.colored_maze.get_color_vector("b")
        self.color_vectors["y"] = self.colored_maze.get_color_vector("y")

        # Get the direction matrices for each possible direction. Allows us to consider where the robot is moving
        #   (if we want)
        self.direction_matrices = dict()
        self.direction_matrices["N"] = self.colored_maze.get_direction_matrix("N")
        self.direction_matrices["E"] = self.colored_maze.get_direction_matrix("E")
        self.direction_matrices["S"] = self.colored_maze.get_direction_matrix("S")
        self.direction_matrices["W"] = self.colored_maze.get_direction_matrix("W")

    # We assume that we can be in any floor location of the maze with equal probability
    def get_initial_state(self):
        total_valid_locations = 0
        # Initialize the list with floats
        initial_state = [0.0 for _ in range(self.colored_maze.width * self.colored_maze.height)]
        for i in range(len(initial_state)):
            if self.colored_maze.is_floor_index(i):
                # We mark that this is a floor space
                initial_state[i] = 1.0
                total_valid_locations += 1

        # Set the probabilities of all floor spaces to be equal (and add up to one)
        for i in range(self.colored_maze.width * self.colored_maze.height):
            # This is a valid (non-wall) spot on the maze
            if initial_state[i] == 1:
                initial_state[i] = 1 / total_valid_locations
            else:
                initial_state[i] = (1 / total_valid_locations) / 100

        return np.array(initial_state)

    # Given an array of sensor readings, return the probability distribution of where we are across the maze
    # Parameter: A list of chars in {'r', 'g', 'b', 'y'} as sensor readings
    # Optional Parameter: A list of moves as {'N', 'E', 'S', 'W'} as the moves the robot has taken
    # The lengths of both lists must be the same is movements are provided
    def solve_for_probability_distribution(self, sensor_readings, movements=None):
        if movements:
            if len(sensor_readings) != len(movements):
                print("Movements and sensor readings must be the same length", file=sys.stderr)
                return None
        current_state = self.initial_state
        for i in range(len(sensor_readings)):
            if movements:
                current_state = self.get_next_state(current_state, sensor_readings[i], movements[i])
            else:
                current_state = self.get_next_state(current_state, sensor_readings[i])

        return current_state

    # Assuming the robot moves randomly, we can create a matrix of where a robot could move
    # Each row represents the starting position, and the column represents where the robot could end up
    def random_movement_matrix(self):
        # To help keep things concise
        w = self.colored_maze.width
        h = self.colored_maze.height

        movement_matrix = np.array([[float(0.0) for _ in range(w * h)] for _ in range(w * h)])

        for loc in range(w * h):
            # Check if this space is a floor tile
            if self.colored_maze.is_floor_index(loc):
                # Get the possible locations we could have moved (or not moved - hitting a wall)
                possible_locations = self.colored_maze.blind_movements_indices(loc)
                # This allows for repeated locations. If we have two walls bordering loc, the probability of
                #   staying in the same spot is 0.5
                for move_loc in possible_locations:
                    movement_matrix[loc][move_loc] += 0.25

        return movement_matrix

    # Given a previous state of probabilities and new sensor data, return the next probability state
    def get_next_state(self, prev_state, sensor_data, move=None):
        predicted_state = self.prediction_step(prev_state, move)

        # Get the next state's unadjusted values
        next_state = self.sensor_update_step(predicted_state, sensor_data)

        # Now we adjust this to that it is a probability distribution (adds up to 1)
        adjustment = 1 / sum(next_state)
        for i in range(len(next_state)):
            next_state[i] *= adjustment

        return next_state

    # Given a previous state of probabilities, multiply that by the movement matrix to get the predicted state
    #   without accounting for the sensor
    def prediction_step(self, prev_state, move=None):
        # See if we know which direction we tried to move in
        if move:
            return np.matmul(self.direction_matrices[move], prev_state)

        # If not, assume we moved a random direction
        return np.matmul(self.movement_matrix, prev_state)

    # Given the predictions and the sensor data, return the predicted state that aligns with the sensor data
    def sensor_update_step(self, predictions, sensor_data):
        return predictions * self.color_vectors[sensor_data]


if __name__ == "__main__":
    Fil = FilteringMazePredictor(ColoredMaze("./mazes/maze1"))
    # print(Fil.movement_matrix)
    probs = Fil.solve_for_probability_distribution(["r", "g", "r", "g", "b"])
    Fil.colored_maze.illustrate_probabilities(probs)
