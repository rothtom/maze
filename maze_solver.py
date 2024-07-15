import sys
import re
import maze_generator as mg
from maze_generator import Cell, DIRECTIONS
from visualizer import load_maze

def main():
    USAGE = "python3 maze_solver.py {solvong algorythm}"
    clas = re.split(r".* python3?", " ".join(sys.argv))
    clas = clas[-1].split()
    if len(clas) != 2:
        sys.exit(USAGE)

    maze = load_maze()
    if clas[-1] == "right_hand":
        path = right_hand()

def right_hand(maze):
    cell = maze[0][0]
    path = []
    path.append(cell)
    cell = mg.get_cell_from_direction(cell.get_empty_walls[0])
    while True:
        possible_ways = cell.get_empty_walls()
        possible_ways.remove(entrypoint)
        index = DIRECTIONS.index(entrypoint)

        path.append(cell)



if __name__ == "__main__":
    main()