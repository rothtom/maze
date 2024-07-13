import pygame as pg

HEIGHT = 1280
WIDTH = 720

pg.init()
screen = pg.display.set_mode(HEIGHT, WIDTH)
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event