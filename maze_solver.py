import sys
import re

from maze_generator import DIRECTIONS
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
    while True:
        possible_ways = get_possible_ways(cell)
        path.append(cell)


def get_possible_ways(cell):


if __name__ == "__main__":
    main()