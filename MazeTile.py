import cs1lib

# Author: Ben Williams '25
# Date: November 1st, 2023


class MazeTile:
    def __init__(self, colored_maze, maze_x, maze_y, maze_start_x, maze_start_y):
        self.colored_maze = colored_maze
        # The tiles location within the maze
        self.maze_x = maze_x
        self.maze_y = maze_y
        self.color = colored_maze.get_color(maze_x, maze_y)

        # The x,y location of where the maze starts on the window
        self.maze_start_x = maze_start_x
        self.maze_start_y = maze_start_y

    def draw(self, window_height, probability_text):
        tile_offset = (window_height / max(self.colored_maze.height, self.colored_maze.width)) * 0.8
        tile_start_x = self.maze_start_x + tile_offset * self.maze_x
        tile_start_y = self.maze_start_y - tile_offset * self.maze_y
        cs1lib.set_stroke_width(3)
        cs1lib.set_stroke_color(1, 1, 1)

        if self.color == "r":
            cs1lib.set_fill_color(0.8, 0, 0)
        elif self.color == "g":
            cs1lib.set_fill_color(0, 0.7, 0)
        elif self.color == "b":
            cs1lib.set_fill_color(0, 0, 0.8)
        elif self.color == "y":
            cs1lib.set_fill_color(0.8, 0.8, 0)
        else:
            cs1lib.set_fill_color(0, 0, 0)

        cs1lib.draw_rectangle(tile_start_x, tile_start_y, tile_offset, tile_offset)

        cs1lib.set_fill_color(1, 1, 1)
        cs1lib.set_font_size(tile_offset / 4.5)
        if self.color:
            cs1lib.draw_text(probability_text, tile_start_x + tile_offset / 6, tile_start_y + tile_offset / 2 + 5)


    def __str__(self):
        if self.color:
            return "Tile at: (" + str(self.maze_x) + ", " + str(self.maze_y) + ") with color " + self.color
        else:
            return "Wall Tile at: (" + str(self.maze_x) + ", " + str(self.maze_y) + ")"

