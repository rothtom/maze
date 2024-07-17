import sys
import re
import csv
import math
import copy
import maze_generator as mg
from maze_generator import Cell, DIRECTIONS
from visualizer import load_maze

class AStarCell(Cell):
    def __init__(self, cell):
        self.wall = cell.wall
        self.x = cell.x
        self.y = cell.y
        self.target = cell.target
        self.manhattan_distance = manhattan_distance(self, maze[target[0]][target[1]])
        self.path_cost = None
        self.cost = None
        self.explored = False
        self.parent = None
        self.dead_end = False
    
    def calculate_fcost(self):
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
        explored_cells = path
    elif algorythm == "a_star":
        explored_cells, path = a_star(maze)
    elif algorythm == "dijkstras":
        explored_cells, path = dijkstras(maze)
    elif algorythm == "dead_end_fill":
        explored_cells, path = dead_end_fill(maze)
    else:
        sys.exit("Invalid solving algorythm")
    
    with open(f"./maze/solution/{clas[-1]}_path.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["x", "y"])
        writer.writeheader()
        for cell in path:
            writer.writerow({"x": cell[0],
                             "y": cell[1],
                             })
            
    with open(f"./maze/solution/{clas[-1]}_explored.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["x", "y"])
        writer.writeheader()
        for cell in explored_cells:
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
    cell.path_cost = 10
    cell.calculate_fcost()
    explored_cells = [[cell.x, cell.y]]
    considered_cells = [cell]
    while cell.target == False and len(considered_cells) > 0:
        cell = sorted(considered_cells, key=lambda x: x.cost, reverse=False)[0]
        considered_cells.remove(cell)
        cell.explored = True
        for direction in cell.get_empty_walls():
            neighbor_cords = cell.get_cell_in_direction(direction)
            neighbor = maze[neighbor_cords[0]][neighbor_cords[1]]
            if neighbor.path_cost != None:
                if cell.path_cost > neighbor.path_cost:
                    continue
            else:
                neighbor.path_cost = cell.path_cost + 10
                neighbor.calculate_fcost()
                neighbor.parent = cell
                considered_cells.append(neighbor)
        explored_cells.append([cell.x, cell.y])

    cell = maze[target[0]][target[1]]
    path = [[cell.x, cell.y]]
    while cell.parent != None:
        cell = cell.parent
        path.append([cell.x, cell.y])
    path.reverse()
    return explored_cells, path

    

def manhattan_distance(cell, target):
    cost = [(target.x - cell.x), (target.y - cell.y)]
    if cost[0] < 0:
        cost[0] = cost[0] * -1
    if cost[1] < 0:
        cost[1] = cost[1] * - 1
    # if (cost[0] * cost[0]) + (cost[1] * cost[1]) == 0:
        # return 0
    # return (math.sqrt((cost[0] * cost[0]) + (cost[1] * cost[1]))) * 10
    return (cost[0] + cost[1]) * 10

def dijkstras(maze):
    unvisited = []
    explored = []
    for i in range(SIZEX):
        for j in range(SIZEY):
            maze[i][j] = AStarCell(maze[i][j])
            unvisited.append(maze[i][j])
            explored.append([maze[i][j].x, maze[i][j].y])

    cell = maze[STARTX][STARTY]
    cell.cost = 0
    visited = []
    next_cells = []
    while len(unvisited) > 1:
        neighbors = get_connected_cells(maze, cell)
        for neighbor in neighbors:
            if neighbor in unvisited:
                next_cells.append(neighbor)
            if neighbor.cost != None:
                if neighbor.cost < cell.cost + 1:
                    continue
            neighbor.cost = cell.cost + 1
            neighbor.parent = cell
        visited.append(cell)
        unvisited.remove(cell)
        cell = sorted(next_cells, key=lambda x: x.cost, reverse=True)[0]
        next_cells.remove(cell)
        



    cell = maze[target[0]][target[1]]
    path = []
    while cell.parent != None:
        path.append([cell.x, cell.y])
        cell = cell.parent
    path.append([cell.x, cell.y])
    path.reverse()
    return explored, path



def get_connected_cells(maze, cell):
    neighbor_cells = []
    for direction in cell.get_empty_walls():
        cell_cords = cell.get_cell_in_direction(direction)
        neighbor_cells.append(maze[cell_cords[0]][cell_cords[1]])
    return neighbor_cells

def dead_end_fill(maze):
    unvisited = []
    dead_ends = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            maze[i][j] = AStarCell(maze[i][j])
            unvisited.append(maze[i][j])
            if len(maze[i][j].get_empty_walls()) == 1:
                dead_ends.append(maze[i][j])
                maze[i][j].dead_end = True
    dead_ends.remove(maze[start[0]][start[1]])
    dead_ends.remove(maze[target[0]][target[1]])

    explored = []
    while len(dead_ends) > 0:
        cell = dead_ends[0]
        dead_ends.remove(cell)
        directions = cell.get_empty_walls()
        for direction in directions:
            neighbor_cords = cell.get_cell_in_direction(direction)
            neighbor = maze[neighbor_cords[0]][neighbor_cords[1]]
            options = len(neighbor.get_empty_walls())
            for direction2 in neighbor.get_empty_walls():
                neighbor2_cords = neighbor.get_cell_in_direction(direction2)
                neighbor2 = maze[neighbor2_cords[0]][neighbor2_cords[1]]
                if neighbor2.dead_end:
                    options -= 1
            if options == 1:
                neighbor.dead_end = True
                cell = neighbor  
                if [cell.x, cell.y] not in explored:
                    dead_ends.append(cell)
                    explored.append([cell.x, cell.y])
                    unvisited.remove(cell)

            
    cell = maze[start[0]][start[1]]
    path = [[cell.x, cell.y]]
    while cell.target == False:
        for direction in cell.get_empty_walls():
            neighbor_cords = cell.get_cell_in_direction(direction)
            neighbor = maze[neighbor_cords[0]][neighbor_cords[1]]
            if  neighbor in unvisited and [neighbor.x, neighbor.y] not in path:
                path.append([cell.x, cell.y])
                cell = neighbor
    return explored, path




if __name__ == "__main__":
    main()