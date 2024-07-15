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
        path = right_hand(maze)

def right_hand(maze):
    cell = maze[0][0]
    path = []
    path.append(cell)
    exitpoint = cell.get_empty_walls()[0]
    cell_cords = cell.get_cell_in_direction(exitpoint)
    cell = maze[cell_cords[0]][cell_cords[1]]
    entrypoint = mg.opposite_direction(exitpoint)
    while True:
        possible_ways = cell.get_empty_walls()
        index = DIRECTIONS.index(entrypoint)
        for i in range(len(DIRECTIONS)):
            exitpoint = DIRECTIONS[index - i]
            if exitpoint in possible_ways:
                cell_cords = cell.get_cell_in_direction(exitpoint)
                cell = maze[cell_cords[0]][cell_cords[1]]
                entrypoint = mg.opposite_direction(exitpoint)
                path.append(cell)
        print(cell.x, cell.y)
        if cell.target:
            print(path)
            return path

        path.append(cell)



if __name__ == "__main__":
    main()