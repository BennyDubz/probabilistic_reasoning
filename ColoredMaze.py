import sys
import random
import numpy as np

# Author: Ben Williams '25
# Date: October 26th, 2023

# Many of these methods are nearly identical to the Maze.py function made by the Dartmouth CS staff
#   when designing the earlier Mazeworld assignment. Though this maze representation is different,
#   some of its code is helpful for instantiating this colored maze


# An implementation of a maze that allows spaces to be colored
class ColoredMaze:
    def __init__(self, maze_file_loc):
        self.robot_loc = []
        try:
            with open(maze_file_loc, "r") as f:
                lines = []
                for line in f:
                    line = line.strip()

                    # Ignore blank lines
                    if len(line) == 0:
                        pass
                    # Robot command
                    elif line[0] == "\\":
                        params = line.split()
                        robot_x = int(params[1])
                        robot_y = int(params[2])

                        self.robot_loc.append(robot_x)
                        self.robot_loc.append(robot_y)
                    else:
                        lines.append(line)

                self.width = len(lines[0])
                self.height = len(lines)
                self.maze_map = list("".join(lines))
        except FileNotFoundError:
            print(f'File {maze_file_loc} not found', file=sys.stderr)
            self.width = 0
            self.height = 0
            self.maze_map = []

    # Returns the index value in the maze map based on x, y coordinates
    def index(self, x, y):
        return (self.height - y - 1) * self.width + x

    # Get the color at a given spot on the maze. Returns None if out of bounds or is a wall
    def get_color(self, x, y):
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None

        loc = self.index(x, y)

        # Wall space
        if self.maze_map[loc] == "#":
            return None
        else:
            return self.maze_map[loc]

    # Returns a boolean of whether the location is a floor space (True) or a wall (False)
    # Takes x, y coordinates as parameters
    def is_floor_xy(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        return self.maze_map[self.index(x, y)] != "#"

    # Returns a boolean of whether the location is a floor space (True) or a wall (False)
    # Takes an index as parameter
    def is_floor_index(self, index):
        if index < 0 or index >= self.width * self.height:
            return False

        return self.maze_map[index] != "#"

    # Renders the robot locations onto the maze
    def create_render_list(self):
        render_list = list(self.maze_map)

        robot_number = 0

        # Needed to add the -1 in order to account for the turn element in the state
        for index in range(0, len(self.robot_loc) - 1, 2):

            x = self.robot_loc[index]
            y = self.robot_loc[index + 1]

            render_list[self.index(x, y)] = self._robot_char(robot_number)
            robot_number += 1

        return render_list

    # Illustrates the maze as ascii art
    def __str__(self):

        # render robot locations into the map
        render_list = self.create_render_list()

        # use the render_list to construct a string, by
        #  adding newlines appropriately

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):

                s += render_list[self.index(x, y)]

            s += "\n"

        return s

    # Get the color, but add the noise of the imperfect sensor (88% correct, 12% one of the other colors)
    def get_color_faulty(self, x, y):
        actual_color = self.get_color(x, y)
        if actual_color == "#":
            return actual_color

        # The sensor works as intended 88% of the time
        if random.random() <= 0.88:
            return actual_color

        # Return a random color from the list that is not the actual color
        color_list = ["r", "g", "b", "y"]
        color_list.remove(actual_color)
        return random.choice(color_list)

    # Returns a list of the possible movements in index format (1D array, not x,y)
    # This also considers running into a wall and staying in the same space
    # If the robot has more than one move that hits a wall, the original location
    #   will appear more than once in the possible_locations returned
    def blind_movements_indices(self, index):
        possible_locations = []
        x = index % self.width
        y = self.height - index // self.width - 1
        for x_mov in range(-1, 2):
            for y_mov in range(-1, 2):
                if abs(x_mov) + abs(y_mov) > 1 or (x_mov == 0 and y_mov == 0):
                    continue
                if self.is_floor_xy(x + x_mov, y + y_mov):
                    possible_locations.append(self.index(x + x_mov, y + y_mov))
                else:
                    possible_locations.append(index)

        return possible_locations

    # Using the 0.88 for the sensor accuracy
    def get_color_vector(self, color):
        vector = np.zeros(self.width * self.height)
        for x in range(self.width):
            for y in range(self.height):
                tile_color = self.get_color(x, y)
                if tile_color == color:
                    vector[self.index(x, y)] = 0.88
                elif tile_color:
                    vector[self.index(x, y)] = 0.04
                # else:
                #     vector[self.index(x, y)] = 0.00001

        return vector

    # Given a direction, we can compute a matrix of all the locations where we could in
    #   be if we moved in that direction. Rows represent the start index, columns represent the end index
    def get_direction_matrix(self, direction):
        direction_matrix = np.zeros((self.width * self.height, self.width * self.height))
        x_mov = 0
        y_mov = 0
        # Handle which direction we are looking at
        if direction == "N":
            y_mov = 1
        elif direction == "E":
            x_mov = 1
        elif direction == "S":
            y_mov = -1
        elif direction == "W":
            x_mov = -1

        for x in range(self.width):
            for y in range(self.height):
                # We can move in this direction from this space
                if self.is_floor_xy(x + x_mov, y + y_mov):
                    direction_matrix[self.index(x, y)][self.index(x + x_mov, y + y_mov)] = 1
                # We hit a wall or the edge and stay still
                else:
                    direction_matrix[self.index(x, y)][self.index(x, y)] = 1

        return direction_matrix

    @staticmethod
    # Returns the character of a given robot number
    def _robot_char(robot_number):
        return chr(ord("A") + robot_number)

    # Given a probability state, illustrate it on the maze
    def illustrate_probabilities(self, probability_state):
        num_length = 5
        string = "| "
        curr_col = 0
        for i in range(len(probability_state)):
            if curr_col == self.width:
                curr_col = 0
                string += "\n| "
            cell_info = self.maze_map[i] + ": "
            if probability_state[i] < 10 ** -(num_length - 1):
                if probability_state[i] > 5 * 10 ** -num_length:
                    cell_info += "0.0001"
                else:
                    cell_info += "0.0000"
            else:
                print_num = str(probability_state[i])[:num_length]
                while len(print_num) <= num_length:
                    print_num += "0"
                cell_info += print_num

            cell_info += " | "
            string += cell_info
            curr_col += 1
        print(string)

    # Given a direction, try to move the first robot there
    # If we hit a wall, do not do anything
    def attempt_robot_move(self, direction):
        if direction == "N":
            if self.is_floor_xy(self.robot_loc[0], self.robot_loc[1] + 1):
                self.robot_loc[1] += 1
        elif direction == "E":
            if self.is_floor_xy(self.robot_loc[0] + 1, self.robot_loc[1]):
                self.robot_loc[0] += 1
        elif direction == "S":
            if self.is_floor_xy(self.robot_loc[0], self.robot_loc[1] - 1):
                self.robot_loc[1] -= 1
        elif direction == "W":
            if self.is_floor_xy(self.robot_loc[0] - 1, self.robot_loc[1]):
                self.robot_loc[0] -= 1

    # Puts one robot at a random location on the maze
    # If there are other robots, they will be removed
    def randomize_robot_location(self):
        # Put the robot on some random empty floor space
        floor_loc = []
        for x in range(self.width):
            for y in range(self.height):
                if self.is_floor_xy(x, y):
                    floor_loc.append((x, y))
        robot_loc = random.choice(floor_loc)
        # Set the robot locations to their appropriate values in the colored maze
        self.robot_loc = []
        self.robot_loc.append(robot_loc[0])
        self.robot_loc.append(robot_loc[1])

if __name__ == "__main__":
    maze1 = ColoredMaze("./mazes/maze1")
    print(maze1)
    # print(maze1.get_color(1, 1))
    print(maze1.get_color(0, 0))
    # print(maze1.get_color(1, 0))
    # print("------")
    # sensor_readings = []
    # for _ in range(100):
    #     sensor_readings.append(maze1.get_color_faulty(1, 1))
    # print(sensor_readings)

    print(maze1.blind_movements_indices(1))
