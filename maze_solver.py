import sys
import re
import csv
import math
import maze_generator as mg
from maze_generator import Cell, DIRECTIONS
from visualizer import load_maze

class AStarCell(Cell):
    def __init__(self, cell):
        self.wall = cell.wall
        self.x = cell.x
        self.y = cell.y
        self.target = cell.target
        self.manhattan_distance = manhattan_distance(self, target)
        self.path_cost = None
        self.cost = None
        self.explored = False
    
    def calculate_cost(self):
        self.cost = self.manhattan_distance + self.path_cost

def main():
    USAGE = "python3 maze_solver.py {solvong algorythm}"
    clas = re.split(r".* python3?", " ".join(sys.argv))
    clas = clas[-1].split()
    if len(clas) != 2:
        sys.exit(USAGE)

    with open("./maze/recursive/mazedata.csv", "r") as df:
        reader = csv.DictReader(df)
        for row in reader:
            global mazedata
            mazedata = row
    global maze
    maze = load_maze()
    global target
    target = [int(mazedata["TARGETX"]), int(mazedata["TARGETY"])]
    target = maze[int(target[0])][int(target[1])]
    global SIZEX
    SIZEX = int(mazedata["SIZEX"])
    global SIZEY
    SIZEY = int(mazedata["SIZEY"])
    global STARTX
    STARTX = int(mazedata["STARTX"])
    global STARTY
    STARTY = int(mazedata["STARTY"])
    global start
    start = [STARTX, STARTY]
    
    algorythm = clas[-1]
    if algorythm == "right_hand":
        path = right_hand(maze)
    elif algorythm == "a_star":
        path = a_star(maze)
    else:
        sys.exit("Invalid solving algorythm")
    
    with open(f"./maze/solution/{clas[-1]}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["x", "y"])
        writer.writeheader()
        for cell in path:
            writer.writerow({"x": cell[0],
                             "y": cell[1],
                             })
        
    


def right_hand(maze):
    path = []
    start = maze[0][0]
    path.append([start.x, start.y])
    direction = start.get_empty_walls()[0]
    cell_cords = start.get_cell_in_direction(direction)
    cell = maze[cell_cords[0]][cell_cords[1]]
    path.append([cell.x, cell.y])
    while cell.target == False:
        direction = get_rightest_wall(cell, direction)
        cell_cords = cell.get_cell_in_direction(direction)
        cell = maze[cell_cords[0]][cell_cords[1]]
        path.append([cell.x, cell.y])
    return path

def get_rightest_wall(cell, direction):
    possible_ways = cell.get_empty_walls()
    if direction == "n":
        orientation = ["e", "n", "w", "s"]
    elif direction == "e":
        orientation = ["s", "e", "n", "w"]
    elif direction == "s":
        orientation = ["w", "s", "e", "n"]
    elif direction == "w":
        orientation = ["n", "w", "s", "e"]
    else:
        raise ValueError
    
    for way in orientation:
        if way in possible_ways:
            return way

def a_star(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            maze[i][j] = AStarCell(maze[i][j])
    cell = maze[0][0]
    cell.path_cost = 0
    cell.calculate_cost()
    path = []
    while cell.target == False:
        directions = cell.get_empty_walls()
        neighbors = []
        for direction in directions:
            cords = cell.get_cell_in_direction((direction))
            neighbors.append(maze[cords[0]][cords[1]])
        for neighbor in neighbors:
            neighbor.path_cost = cell.path_cost + 10
            neighbor.calculate_cost()
        lowest_path_cost = int(((int(mazedata["SIZEX"])) * int(mazedata["SIZEY"])) + 1) * 10
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j].cost != None and maze[i][j].explored == False:
                    if maze[i][j].cost < lowest_path_cost:
                        best_cell = maze[i][j]
                        lowest_path_cost = best_cell.cost
        cell = best_cell
        cell.explored = True
        path.append([cell.x, cell.y])
    return path

def manhattan_distance(cell, target):

    cost = [(target.x - cell.x), (target.y - cell.y)]
    if cost[0] < 0:
        cost[0] = cost[0] * -1
    if cost[1] < 0:
        cost[1] = cost[1] * - 1
    if (cost[0] * cost[0]) + (cost[1] * cost[1]) == 0:
        return 0
    return (math.sqrt((cost[0] * cost[0]) + (cost[1] * cost[1]))) * 10



if __name__ == "__main__":
    main()