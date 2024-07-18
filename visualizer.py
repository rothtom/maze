import pygame as pg
import os
import sys
import csv
import copy
from maze_generator import Cell


WIDTH= 1280
HEIGHT = 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
MAZETYPE = "recursive"
# solving_algorythm = "a_star"
# used to set default. Decides which folder to use (load). Can change this with clas
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
        self.is_path = False
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
        elif self.is_path:
            pg.draw.rect(screen, "blue", cell)
        elif not self.is_path:
            pg.draw.rect(screen, "black", cell)
            if self.explored:
                pg.draw.rect(screen, "orange", cell)
        for d in wall.keys():
            if wall[d]:
                pg.draw.rect(screen, "green", wall[d])

    def show_path(self):
        self.is_path = True

    def hide_path(self):
        self.is_path = False

    def mark_current(self):
        cell = pg.Rect(self.x * TILE[0] + TILE[0] * 0.1, self.y * TILE[1] + TILE[1] * 0.1, TILE[0] * 0.8, TILE[1] * 0.8)
        pg.draw.rect(screen, "pink", cell)
    
    def show_explored(self):
        self.explored = True

    def hide_explored(self):
        self.explored = False

def main():
    if len(sys.argv) > 3:
        sys.exit("invalid clas!")
    try:
        solving_algorythm = sys.argv[1]
    except IndexError:
        solving_algorythm = "a_star"
        # set default solving algorythm if non in clas
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
    for cell in explored_cells:
        maze[cell[0]][cell[1]].explored = True
    show_explored_cells = False

    path_step = 0
    path_length = len(path)
    show_entire_path = False
    explored_step = 0
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_RIGHT:
                    if path_step < path_length - 1:
                        path_step += 1
                        
                elif event.key == pg.K_LEFT:
                    if path_step > 0:
                        path_step -= 1   
                
                elif event.key == pg.K_TAB:
                    show_entire_path = show_entire_path == False

                elif event.key == pg.K_SPACE:
                    show_explored_cells = show_explored_cells == False
                    if not show_explored_cells:
                        explored_step = 0
                
                elif event.key == pg.K_a:
                    if explored_step > 0:
                        explored_step -= 1
                elif event.key == pg.K_d:
                    if explored_step < len(explored_cells) - 1:
                        explored_step += 1

            for i in range(SIZEX):
                for j in range(SIZEY):
                    maze[i][j].pixel_cell()
                    try:
                        cords = [maze[i][j].x, maze[i][j].y]
                        if not show_entire_path:
                            if path.index(cords) < path_step:
                                maze[i][j].show_path() 
                            else:
                                maze[i][j].hide_path()
                        else:
                            for cords in path:
                                maze[cords[0]][cords[1]].show_path()
                    except ValueError:
                        pass
                    try:
                        cords = [maze[i][j].x, maze[i][j].y]
                        if not show_explored_cells:
                            if explored_cells.index(cords) < explored_step:
                                maze[i][j].show_explored() 
                            else:
                                maze[i][j].hide_explored()
                        else:
                            for cords in explored_cells:
                                maze[cords[0]][cords[1]].show_explored()
                    except ValueError:
                        pass

            maze[path[path_step][0]][path[path_step][1]].mark_current()
        
                
        pg.display.flip()
        clock.tick(60)
    pg.quit()

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

    #i = 78
    # possibility to show specific image
    with open(f"maze/{MAZETYPE}/complete.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            maze[int(row["x"])][int(row["y"])] = Cell(row["x"], row["y"], row["wall_n"], row["wall_e"], row["wall_s"], row["wall_w"], row["target"])
    return maze


if __name__ == "__main__":
    main()