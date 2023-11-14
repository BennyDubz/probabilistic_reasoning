from MazeTile import MazeTile
from cs1lib import *
from ColoredMaze import ColoredMaze
from FilteringMazePredictor import FilteringMazePredictor

# Author: Ben Williams '25
# Date: November 1st, 2023

################################################################################################################
# I was using the old library that we got in our intro computer science (CS1) class for all the graphics.
#   so I had to do some weird stuff in order to get the text to line up and everything. Not exactly the best
#   code in the world, but still a cool demonstration of the filtering algorithm
################################################################################################################

# Boolean variables to help run the program
start_program = True
made_move = True
cleared = False
robot_knows_moves = False
changed_robot_knows_moves = True

# Size of the window
window_width = 1200
window_height = 800

# Creating the maze's and the filtering algorithm's objects
maze_folder = "./mazes/"
maze_list = ["maze4x4", "maze1", "quadrants", "separatedQuadrants", "disconnectedComponents", "maze8x8", "maze16x16", "maze16x16Even"]
# We will swap into the first maze
current_maze = -1

# Initializing so that they are global variables
colored_maze = ColoredMaze(maze_folder + maze_list[current_maze])
Fil = FilteringMazePredictor(colored_maze)
colored_maze.randomize_robot_location()

# Initial probability distribution is equal probability for each square
prob_dist = Fil.initial_state
directions = []
colors_sensed = []


# Used by the cs1lib start graphics
def main():
    global start_program, made_move, cleared, prob_dist, changed_robot_knows_moves

    # Only run at the start of the program
    if start_program or cleared:
        start_program = False
        set_clear_color(0, 0, 0)
        set_stroke_color(1, 1, 1)
        clear()
        set_font_size(16)
        draw_text("The robot begins at a random location in the maze. Black squares are walls.", window_width / 40,
                  window_height / 40)
        draw_text("Use WASD keys to move. Probability distribution is shown on the squares", window_width / 40,
                  window_height / 20)
        draw_text("Press m to change mazes", window_width / 40,
                   3 * window_height / 40)

    if changed_robot_knows_moves:
        set_stroke_color(0, 0, 0)
        set_fill_color(0, 0, 0)
        draw_rectangle(0, 9.1 * window_height/10, window_width / 2, window_height / 10)

        set_font_size(16)
        set_stroke_color(1, 1, 1)
        set_fill_color(1, 1, 1)
        knows_text = "Robot knows the moves it makes: " + str(robot_knows_moves) + ". Press k to flip this then make a move"
        draw_text(knows_text, window_width / 40, 19 * window_height / 20)

        changed_robot_knows_moves = False


    # If we have made a move (or are beginning the gui and want to draw the maze)
    if made_move:
        # Attempt the move and get the new probabilities with the new sensor reading
        if len(directions) > 0:
            colored_maze.attempt_robot_move(directions[len(directions) - 1])
            sensor_reading = colored_maze.get_color_faulty(colored_maze.robot_loc[0], colored_maze.robot_loc[1])
            colors_sensed.append(sensor_reading)
            if robot_knows_moves:
                prob_dist = Fil.solve_for_probability_distribution(colors_sensed, directions)
            else:
                prob_dist = Fil.solve_for_probability_distribution(colors_sensed)

        # Draw all the maze tiles
        for tile in maze_tiles:
            index = colored_maze.index(tile.maze_x, tile.maze_y)
            probability = prob_dist[index]
            prob_string = probability_string(probability)
            tile.draw(window_height, prob_string)

        # Show the last color sensed and the actual robot location
        if len(colors_sensed) > 0:
            # The convoluted way to reset the text without clearing everything
            set_fill_color(0, 0, 0)
            set_stroke_color(0, 0, 0)
            draw_rectangle(7.9 * window_width / 10, 0, 300, 100)

            set_fill_color(1, 1, 1)
            set_stroke_color(1, 1, 1)

            # Show which color was sensed
            set_font_size(16)
            color_text = "Last color sensed: " + colors_sensed[len(colors_sensed) - 1]
            actual_color = colored_maze.get_color(colored_maze.robot_loc[0], colored_maze.robot_loc[1])
            color_text += " accurately" if colors_sensed[len(colors_sensed) - 1] == actual_color else " inaccurately"
            draw_text(color_text, 9 * window_width / 10 - (4 * len(color_text)), window_height / 20)

            robot_loc_text = "Actual robot location: (" + str(colored_maze.robot_loc[0]) + ", " + str(colored_maze.robot_loc[1]) + ")"
            draw_text(robot_loc_text, 9 * window_width / 10 - (4 * len(robot_loc_text)), window_height / 10)

        made_move = False


# Turn the probability into a 5 number long string to have consistent strings
def probability_string(probability):
    num_length = 5
    prob_string = ""
    if probability < 10 ** -(num_length - 1):
        if probability > 5 * 10 ** -num_length:
            prob_string += "0.0001"
        else:
            prob_string += "0.0000"
    else:
        print_num = str(probability)[:num_length + 1]
        while len(print_num) <= num_length:
            print_num += "0"
        prob_string += print_num
    return prob_string


# Switches to the next maze and resets all the maze-related sensors
def swap_maze():
    global current_maze, colored_maze, Fil, prob_dist, directions, colors_sensed, maze_tiles, maze_start_x
    current_maze = (current_maze + 1) % len(maze_list)
    colored_maze = ColoredMaze(maze_folder + maze_list[current_maze])
    colored_maze.randomize_robot_location()
    Fil = FilteringMazePredictor(colored_maze)
    prob_dist = Fil.initial_state
    directions = []
    colors_sensed = []

    # Finding the right place to put the maze so that it is centered
    tile_size = window_height / max(colored_maze.height, colored_maze.width) * 0.8
    maze_pixel_width = tile_size * colored_maze.width
    maze_pixel_height = tile_size * colored_maze.height
    maze_window_height_ratio = maze_pixel_height / window_height
    maze_window_width_ratio = maze_pixel_width / window_width
    maze_start_y = window_height - (window_height * (1 - maze_window_height_ratio)) / 2 - tile_size
    maze_start_x = (window_width - window_width * maze_window_width_ratio) / 2

    # Initialize the maze tiles to be drawn
    maze_tiles = []
    for x in range(colored_maze.width):
        for y in range(colored_maze.height):
            new_tile = MazeTile(colored_maze, x, y, maze_start_x, maze_start_y)
            maze_tiles.append(new_tile)


def key_pressed(key):
    global made_move, robot_knows_moves, changed_robot_knows_moves, start_program
    # To prevent an error where you press two keys at the same time
    if len(directions) > len(colors_sensed):
        return

    if key == "w":
        directions.append("N")
        made_move = True
    if key == "a":
        directions.append("W")
        made_move = True
    if key == "s":
        directions.append("S")
        made_move = True
    if key == "d":
        directions.append("E")
        made_move = True
    if key == "k":
        robot_knows_moves = not robot_knows_moves
        changed_robot_knows_moves = True
    if key == "m":
        swap_maze()
        changed_robot_knows_moves = True
        start_program = True
        made_move = True

# Switch into the first maze
swap_maze()
start_graphics(main, width=window_width, height=window_height, key_press=key_pressed)
