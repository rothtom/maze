import pygame as pg
import os
import csv
import copy


WIDTH= 1280
HEIGHT = 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
MAZETYPE = "recursive"
# decides which folder to use (load)
SQUARE = False
if SQUARE:
    HEIGHT = WIDTH
# enables settings for a square screen

class Cell():
    def __init__(self, x, y, n, e, s, w, target):
        self.wall = {"n": n == "True", 
                     "e": e == "True", 
                     "s": s == "True", 
                     "w": w == "True"}
        self.x = int(x)
        self.y = int(y)
        self.target = target == "True"

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
        else:
            pg.draw.rect(screen, "blue", cell)
        for d in wall.keys():
            if wall[d]:
                pg.draw.rect(screen, "green", wall[d])

def main():
    pg.init()
    clock = pg.time.Clock()
    running = True

    maze = load_maze()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            for i in range(SIZEX):
                for j in range(SIZEY):
                    maze[i][j].pixel_cell()
                
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
            global TILE
            TILE = (WIDTH/SIZEX, HEIGHT/SIZEY)


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