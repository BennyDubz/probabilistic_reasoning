import random
# Author: Ben Williams '25
# Date: October 31st, 2023

# Generates a random maze using the below characteristics
# Does not guarantee that the whole maze is in one connected component!

file_name = "./mazes/maze16x16Even"
width = 16
height = 16
red_chance = 0.2
green_chance = 0.2
blue_chance = 0.2
yellow_chance = 0.2
# Remainder of 1 is just a wall

f = open(file_name, "w")

for col in range(width):
    for row in range(height):
        rand_val = random.random()
        if rand_val < red_chance:
            f.write("r")
            continue
        if rand_val < red_chance + green_chance:
            f.write("g")
            continue
        if rand_val < red_chance + green_chance + blue_chance:
            f.write("b")
            continue
        if rand_val < red_chance + green_chance + blue_chance + yellow_chance:
            f.write("y")
            continue
        else:
            f.write("#")
            continue
    f.write("\n")

f.close()


