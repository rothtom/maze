import pygame as pg
import os
import csv
import copy

HEIGHT = 1280
WIDTH = 720


pg.init()
screen = pg.display.set_mode((HEIGHT, WIDTH))
clock = pg.time.Clock()
running = True
i = 0
#open data file
with open("maze/mazedata.csv", "r") as df:
    reader = csv.DictReader(df)
    for row in reader:
        global SIZEX
        SIZEX = int(row["SIZEX"])
        global SIZEY
        SIZEY = int(row["SIZEY"])

while os.path.isfile(("maze/" + str(i + 1) + ".csv")):
    i += 1

# generate maze dimensioned list
maze =  list()
for i in range(SIZEX):
    maze.append([])
    for j in range(SIZEY):
        maze[i].append([])

with open(f"maze/{i}.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        maze[int(row["x"])][int(row["y"])] = row


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        for i in SIZEX:
            for j in SIZEY:
                pg.draw.rect(pg.Surface.blit, "green", pg.Rect(width= WIDTH / SIZEX, height= WIDTH / SIZEY), )
            
        pg.display.flip()
        clock.tick(60)