from levels2b import *
import random

def randomize_crystals():
    # remove all eventually crystals
    for rnum, room in enumerate(layout[1:-1]):
        for row, line in enumerate(room):
            for col, item in enumerate(line):
                if item == "100":
                    layout[rnum][row][col] = " "


    possible_place = []
    for rnum, room in enumerate(layout[1:-1]):
        for row, line in enumerate(room):
            for col, item in enumerate(line):
                # print(item)
                if item == " ":
                    possible_place.append([row, col])
        # print(possible_place)
        x = random.choice(possible_place) # IndexError: list index out of range  
        # print(x)    
        layout[rnum][x[0]][x[1]] = "100" # TypeError: list indices must be integers or slices, not list
        # print(room)
        possible_place = []
    return layout