import sys
import re
import random
import csv

SIZEX = None
SIZEY = None
n = 0
DIRECTIONS = ["n", "e", "s", "w"]
class Cell():
    def __init__(self, x, y):
        self.wall = {"n": False, 
                     "e": False, 
                     "s": False, 
                     "w": False}
        self.empty = True
        self.x = x
        self.y = y
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
    
    #save maze data to csv
    with open(f"maze/{algorythm}/mazedata.csv", "w") as df:
        fieldnames = ["SIZEX", "SIZEY"]
        writer = csv.DictWriter(df, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"SIZEX": SIZEX, "SIZEY": SIZEY})
    
    # initialize empty maze with goven size
    maze = list()
    for i in range(SIZEX):
        maze.append([])
        for j in range(SIZEY):
            maze[i].append([])
            maze[i][j] = Cell(i, j)
    if algorythm == "recursive":
        maze = recursive_init(maze)
        return 0
    
def recursive_init(maze):
    n = 0
    maze[0][0].build_walls()
    save(maze, maze[0][0], n)
    n += 1
    maze = recursive(maze, maze[0][0])
    return maze
    

def recursive(maze, current_cell, reverse=None):
    availabel_neighbors = get_neighbors(maze, current_cell)
    while len(availabel_neighbors) != 0:
        cell = random.choice(availabel_neighbors)
        availabel_neighbors.remove(cell)
        if cell.empty:
            direction = get_direction(start=cell, end=current_cell)
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

def get_neighbors(maze, c):
    # c beeing the cell whos neighbors we observe
    neighbors = []
    if c.x != 0:
        neighbors.append(maze[c.x-1][c.y])
    if c.x != SIZEX - 1:
        neighbors.append(maze[c.x+1][c.y])
    if c.y != 0:
        neighbors.append(maze[c.x][c.y-1])
    if c.y != SIZEY - 1:
        neighbors.append(maze[c.x][c.y+1])
    return neighbors


def get_direction(start, end):
    if start.x < end.x:
        return "e"
    elif start.x > end.x:
        return "w"
    elif start.y < end.y:
        return "n"
    else:
        return "s"

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
        fieldnames = ["x", "y", "wall_n", "wall_e", "wall_s", "wall_w", "empty", "current"]
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
                })
    return 0

            

if __name__ == "__main__":
    main()