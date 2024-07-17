import pygame as pg
import os
import csv
import copy
from maze_generator import Cell


WIDTH= 1280
HEIGHT = 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
MAZETYPE = "recursive"
solving_algorythm = "a_star"
# decides which folder to use (load)
SQUARE = False
if SQUARE:
    HEIGHT = WIDTH
# enables settings for a square screen

class Cell(Cell):
    def __init__(self, x, y, n, e, s, w, target):
        self.wall = {"n": n == "True", 
                     "e": e == "True", 
                     "s": s == "True", 
                     "w": w == "True"}
        self.x = int(x)
        self.y = int(y)
        self.target = target == "True"
        self.explored = False

    def pixel_cell(self):
        cell = pg.Rect(self.x * TILE[0] + TILE[0] * 0.1, self.y * TILE[1] + TILE[1] * 0.1, TILE[0] * 0.8, TILE[1] * 0.8)
        wall = copy.deepcopy(self.wall)
        if self.wall["n"]:
            wall["n"] = pg.Rect(self.x * TILE[0], self.y * TILE[1], TILE[0], TILE[1] * 0.1)
        if self.wall["e"]:
            wall["e"] = pg.Rect(self.x * TILE[0] + (TILE[0] * 0.9), self.y * TILE[1], TILE[0] * 0.1, TILE[1])
        if self.wall["s"]:
            wall["s"] = pg.Rect(self.x * TILE[0], self.y * TILE[1] + TILE[1] * 0.9, TILE[0], TILE[1] * 0.1)
        if self.wall["w"]:
            wall["w"] = pg.Rect(self.x * TILE[0], self.y * TILE[1], TILE[0] * 0.1, TILE[1])
        if self.target:
            pg.draw.rect(screen, "red", cell)
        elif self.explored:
            pg.draw.rect(screen, "blue", cell)
        elif not self.explored:
            pg.draw.rect(screen, "black", cell)
        for d in wall.keys():
            if wall[d]:
                pg.draw.rect(screen, "green", wall[d])

    def mark(self):
        cell = pg.Rect(self.x * TILE[0] + TILE[0] * 0.1, self.y * TILE[1] + TILE[1] * 0.1, TILE[0] * 0.8, TILE[1] * 0.8)
        pg.draw.rect(screen, "pink", cell)
        self.explored = True

    def unmark(self):
        self.explored = False

def main():
    pg.init()
    clock = pg.time.Clock()
    running = True

    maze = load_maze()
    global TILE
    TILE = (WIDTH/SIZEX, HEIGHT/SIZEY)
    path = []
    with open(f"./maze/solution/{solving_algorythm}_path.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            path.append([int(row["x"]), int(row["y"])])
    explored_cells = []
    with open(f"./maze/solution/{solving_algorythm}_explored.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            explored_cells.append([int(row["x"]), int(row["y"])])

    path_step = 0
    path_length = len(path)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    if path_step < path_length - 1:
                        path_step += 1
                elif event.key == pg.K_LEFT:
                    if path_step > 0:
                        path_step -= 1
                        maze[path[path_step][0]][path[path_step][1]].unmark()
            if path_step == path_length - 1:
                print("Hey!")
        for i in range(SIZEX):
            for j in range(SIZEY):
                maze[i][j].pixel_cell()

        maze[path[path_step][0]][path[path_step][1]].mark()
                
        pg.display.flip()
        clock.tick(60)

def load_maze():
    #open data file
    with open("maze/recursive/mazedata.csv", "r") as df:
        reader = csv.DictReader(df)
        for row in reader:
            global SIZEX
            SIZEX = int(row["SIZEX"])
            global SIZEY
            SIZEY = int(row["SIZEY"])

    # generate maze dimensioned list
    maze =  list()
    for i in range(SIZEX):
        maze.append([])
        for j in range(SIZEY):
            maze[i].append([])
    i = 0
    while os.path.isfile("".join(["maze/recursive/", str(i + 1), ".csv"])):
        i += 1

    #i = 78
    # possibility to show specific image
    with open(f"maze/{MAZETYPE}/{i}.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            maze[int(row["x"])][int(row["y"])] = Cell(row["x"], row["y"], row["wall_n"], row["wall_e"], row["wall_s"], row["wall_w"], row["target"])
    return maze


if __name__ == "__main__":
    main()