import sys
import re
import random
import csv
import shutil
import os

sys.setrecursionlimit(100000)
# set max recursion depth


n = 0
DIRECTIONS = ["n", "e", "s", "w"]
START = [0, 0]
TARGET = [-1, -1]
# chance mazes target
class Cell():
    def __init__(self, x, y, target=False, start=False):
        self.wall = {"n": False, 
                     "e": False, 
                     "s": False, 
                     "w": False}
        self.empty = True
        self.x = x
        self.y = y
        self.target = target
        self.start = start
    def build_walls(self, entrypoint=None):
        for key in self.wall.keys():
            self.wall[key] = True
        self.empty = False
        if entrypoint:
            self.wall[entrypoint] = False
        return 0
    def breakdown_wall(self, *directions):
        for direction in directions:
            self.wall[direction] = False
        return 0
    def get_empty_walls(self):
        empty_walls = []
        for d in DIRECTIONS:
            if self.wall[d] == False:
                empty_walls.append(d)
        return empty_walls
    def get_cell_in_direction(self, direction):
        offsets = {"n": (0, -1), "e": (1, 0), "s": (0, 1), "w": (-1, 0)}
        offset = offsets[direction]
        return [self.x + offset[0], self.y + offset[1]]


def main():
    USAGE = "Usage: python3 maze_generator.py {generation algorythm} {maze size (1 number if square)}"
    clas = re.split(r".* python3?", " ".join(sys.argv))
    clas = clas[-1].split()
    if len(clas) not in  [3, 4]:
        sys.exit(USAGE + "1")
    if re.search(r"^python3? mazegenerator\.py .+ [0-9]+ [0-9]*", " ".join(clas)):
        sys.exit(USAGE + "2")
    try:
        global SIZEX
        SIZEX = int(clas[2])
    except TypeError:
        sys.exit("Maze size must be an integer")
    global SIZEY
    if len(sys.argv) < 5:
        SIZEY = SIZEX
    else:
        try:
            SIZEY = int(clas[3])
        except TypeError:
            sys.exit("Maze size must be an integer")
    algorythm = clas[1]
    
    # clear previous maze from folder
    try:
        shutil.rmtree(f"./maze/{algorythm}")
    except FileNotFoundError:
        pass

    # create the folder for the new maze to store
    os.mkdir(f"./maze/{algorythm}")
    # save maze data to csv
    with open(f"maze/{algorythm}/mazedata.csv", "w") as df:
        fieldnames = ["SIZEX", "SIZEY", "TARGETX", "TARGETY", "STARTX", "STARTY"]
        writer = csv.DictWriter(df, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"SIZEX": SIZEX, "SIZEY": SIZEY, "TARGETX": TARGET[0], "TARGETY": TARGET[1], "STARTX": START[0], "STARTY": START[1]})

    # initialize empty maze with given size
    maze = list()
    for i in range(SIZEX):
        maze.append([])
        for j in range(SIZEY):
            maze[i].append([])
            maze[i][j] = Cell(i, j)
    maze[START[0]][START[1]].start = True
    maze[TARGET[0]][TARGET[1]].target = True
    if algorythm == "recursive":
        maze = recursive_init(maze)
        return 0
    else:
        sys.exit("invalid generation algorythm")
    
def recursive_init(maze):
    global n
    n = 0
    maze[0][0].build_walls()
    save(maze, maze[0][0], n)
    n += 1
    maze = recursive(maze, maze[0][0])
    return maze
    

def recursive(maze, current_cell, reverse=None):
    if current_cell.target or current_cell.start:
        try:
            entrypoint = current_cell.get_empty_walls()[0]
            cell_cords = current_cell.get_cell_in_direction(entrypoint)
            cell = maze[cell_cords[0]][cell_cords[1]]
            for neighbor in get_neighbors(maze, current_cell):
                if neighbor.empty:
                    recursive(maze, cell, reverse=entrypoint)
            return maze
        except IndexError:
            pass
    availabel_neighbors = get_neighbors(maze, current_cell)
    while len(availabel_neighbors) != 0:
        cell = random.choice(availabel_neighbors)
        availabel_neighbors.remove(cell)
        if cell.empty:
            direction = get_direction(start=current_cell, end=cell)
            cell.build_walls(entrypoint=(opposite_direction(direction)))
            current_cell.breakdown_wall(direction)
            global n
            save(maze, cell, n)
            n += 1
            recursive(maze, cell)
    reverse_directions = current_cell.get_empty_walls()
    if reverse != None:
        if reverse in reverse_directions:
            reverse_directions.remove(reverse)
    if len(reverse_directions) == 0:
        return maze
    recursive(maze, cell, reverse=reverse_directions[0])

def get_neighbors(maze, c, sizey=None, sizex=None):
    # c beeing the cell whos neighbors we observe
    try:
        sizey = SIZEY
        sizex = SIZEX
    except NameError:
        pass
    neighbors = []
    if c.x != 0:
        neighbors.append(maze[c.x-1][c.y])
    if c.x != sizex - 1:
        neighbors.append(maze[c.x+1][c.y])
    if c.y != 0:
        neighbors.append(maze[c.x][c.y-1])
    if c.y != sizey - 1:
        neighbors.append(maze[c.x][c.y+1])
    return neighbors


def get_direction(start, end):
    if start.x < end.x:
        return "e"
    elif start.x > end.x:
        return "w"
    elif start.y < end.y:
        return "s"
    else:
        return "n"

def opposite_direction(d):
    if d == "n":
        return "s"
    elif d == "s":
        return "n"
    elif d == "w":
        return "e"
    elif d == "e":
        return "w"
    else:
        raise ValueError
    

def save(maze, current_cell, n):
    with open(f"maze/recursive/{n}.csv", "w") as f:
        fieldnames = ["x", "y", "wall_n", "wall_e", "wall_s", "wall_w", "empty", "current",  "start", "target",]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for j in range(SIZEX):
            for i in range(SIZEY):
                if maze[i][j] == current_cell:
                    current = True
                else:
                    current = False
                writer.writerow({
                    "x": maze[i][j].x,
                    "y": maze[i][j].y,
                    "wall_n": maze[i][j].wall["n"],
                    "wall_e": maze[i][j].wall["e"],
                    "wall_s": maze[i][j].wall["s"],
                    "wall_w": maze[i][j].wall["w"],
                    "empty": maze[i][j].empty,
                    "current": current,
                    "start": maze[i][j].start,
                    "target": maze[i][j].target,
                })
    return 0

            

if __name__ == "__main__":
    main()