import random
import time

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.positions = []
        self.maze = self.create_maze()
        self.start = ()
        self.end = ()

    def create_maze(self):
        mz = [[' ' for i in range(self.cols)] for j in range(self.rows)]
        for i in range(self.rows):
            for y in range(self.cols):
                if (i == 0 or i == self.rows-1):
                    mz[i][y] = '#'
                    continue
                if (y == 0 or y == self.rows-1):
                    mz[i][y] = '#'
                    continue
                else:
                    if (y % 2 !=0) and (i % 2 !=0):
                        self.positions.append((i,y))
                    else:
                        mz[i][y] = '#'
        return mz

    def get_neighbors(self, pos):
        '''North, South, East and West Neighbours'''
        neighbors = []
        #North
        if pos[0] - 2 > 0 and self.maze[pos[0]-2][pos[1]] != '#':
            neighbors.append(['N', (pos[0]-2, pos[1])])
        #South
        if pos[0] + 2 < len(self.maze)-1 and self.maze[pos[0]+2][pos[1]] != '#':
            neighbors.append(['S', (pos[0]+2, pos[1])])
        #East
        if pos[1] + 2 < len(self.maze[0])-1 and self.maze[pos[0]][pos[1]+2] != '#':
            neighbors.append(['E', (pos[0], pos[1]+2)])
        #West
        if pos[1] - 2 > 0 and self.maze[pos[0]][pos[1]-2] != '#':
            neighbors.append(['W', (pos[0], pos[1]-2)])
        return neighbors

    def get_neighbors_solver(self, pos):
        '''North, South, East and West Neighbours'''
        neighbors = []
        # North
        if pos[0] - 1 > 0 and self.maze[pos[0] - 1][pos[1]] != '#':
            neighbors.append(['N', (pos[0] - 1, pos[1])])
        # South
        if pos[0] + 1 < len(self.maze) - 1 and self.maze[pos[0] + 1][pos[1]] != '#':
            neighbors.append(['S', (pos[0] + 1, pos[1])])
        # East
        if pos[1] + 1 < len(self.maze[0]) - 1 and self.maze[pos[0]][pos[1] + 1] != '#':
            neighbors.append(['E', (pos[0], pos[1] + 1)])
        # West
        if pos[1] - 1 > 0 and self.maze[pos[0]][pos[1] - 1] != '#':
            neighbors.append(['W', (pos[0], pos[1] - 1)])
        return neighbors

    def print(self):
        for row in self.maze:
            for cell in row:
                print(cell, end='  ')
            print()
        time.sleep(2)
        print()

    def get_start_pos(self):
        return self.start

    def get_end_pos(self):
        return self.end

    def add_start_and_exit(self):
        '''Called after Maze Generation'''
        first_row = self.positions[0][0]
        last_row = self.positions[-1][0]
        first_row_arr = []
        last_row_arr = []
        for i in range(len(self.maze[0])):
            if self.maze[first_row][i] == ' ':
                first_row_arr.append((first_row, i))
            if self.maze[last_row][i] == ' ':
                last_row_arr.append((last_row, i))
        random_start = random.choice(first_row_arr)
        random_end = random.choice(last_row_arr)
        self.maze[random_start[0]][random_start[1]] = 'S'
        self.start = (random_start[0], random_start[1])
        self.maze[random_end[0]][random_end[1]] = 'E'
        self.end = (random_end[0], random_end[1])


def binary_maze_generation(mz):
    '''South & East'''
    maze = mz.maze
    positions = mz.positions
    for position in positions:
        mz.print()
        south = None
        east = None
        if position[0] + 2 < len(maze)-1:
            south = (position[0] + 2, position[1])
        if position[1] + 2 < len(maze[0])-1:
            east = (position[0], position[1]+2)
        if south and east:
            '''0 = South, 1 = East'''
            rand = random.randint(0, 1)
            if rand == 0:
                maze[south[0]-1][south[1]] = ' '
            else:
                maze[east[0]][east[1]-1] = ' '
        elif south:
            maze[south[0]-1][south[1]] = ' '
        elif east:
            maze[east[0]][east[1]-1] = ' '
    mz.add_start_and_exit()

def sidewinder_maze_generation(mz):
    maze = mz.maze
    positions = mz.positions

    run = []
    for position in positions:
        mz.print()
        south = None
        east = None
        if position[0] + 2 < len(maze) - 1:
            south = (position[0] + 2, position[1])
        if position[1] + 2 < len(maze[0]) - 1:
            east = (position[0], position[1] + 2)
        if south and east:
            '''0 = South, 1 = East'''
            rand = random.randint(0, 1)
            if rand == 0:
                if run:
                    rand_run = random.choice(run)
                    run = []
                else:
                    rand_run = ((south[0]-1,south[1]))
                maze[rand_run[0]][rand_run[1]] = ' '
            else:
                maze[east[0]][east[1] - 1] = ' '
                if south:
                    run.append((south[0]-1, south[1]))
        elif south:
            if run:
                rand_run = random.choice(run)
                run = []
            else:
                rand_run = ((south[0] - 1, south[1]))
            maze[rand_run[0]][rand_run[1]] = ' '
        elif east:
            maze[east[0]][east[1] - 1] = ' '
    mz.add_start_and_exit()

def aldous_broder_maze_generation(mz):
    maze = mz.maze
    positions = mz.positions
    cur_pos = random.choice(positions)
    visited = []

    while len(visited) != len(positions):
        neighbors = mz.get_neighbors(cur_pos)
        random_neighbor = random.choice(neighbors)
        move = random_neighbor[0]
        if cur_pos not in visited:
            visited.append(cur_pos)
        if random_neighbor[1] not in visited:
            match move:
                case 'N':
                    maze[random_neighbor[1][0] + 1][random_neighbor[1][1]] = ' '
                case 'S':
                    maze[random_neighbor[1][0] - 1][random_neighbor[1][1]] = ' '
                case 'E':
                    maze[random_neighbor[1][0]][random_neighbor[1][1] - 1] = ' '
                case 'W':
                    maze[random_neighbor[1][0]][random_neighbor[1][1] + 1] = ' '
        cur_pos = random_neighbor[1]
    mz.add_start_and_exit()

def recursive_backtracking_map_generation(mz):
    maze = mz.maze
    positions = mz.positions
    cur_pos = random.choice(positions)
    visited_static = []
    visited_stack = []
    while len(visited_static) != len(positions):
        if cur_pos not in visited_stack:
            visited_stack.append(cur_pos)
        if cur_pos not in visited_static:
            visited_static.append(cur_pos)
        neighbors = mz.get_neighbors(cur_pos)
        filtered_neighbors = []
        for neighbor in neighbors:
            if neighbor[1] not in visited_static:
                filtered_neighbors.append(neighbor)
        if filtered_neighbors:
            random_neighbor = random.choice(filtered_neighbors)
            cur_pos = random_neighbor[1]
            move = random_neighbor[0]
            match move:
                case 'N':
                    maze[random_neighbor[1][0] + 1][random_neighbor[1][1]] = ' '
                case 'S':
                    maze[random_neighbor[1][0] - 1][random_neighbor[1][1]] = ' '
                case 'E':
                    maze[random_neighbor[1][0]][random_neighbor[1][1] - 1] = ' '
                case 'W':
                    maze[random_neighbor[1][0]][random_neighbor[1][1] + 1] = ' '
        else:
            cur_pos = visited_stack[-2]
            visited_stack.pop(-1)
    mz.add_start_and_exit()

def recursive_backtracking_maze_solver(mz):
    maze = mz.maze
    cur_pos = mz.get_start_pos()
    char = '&'
    visited_stack = []
    while maze[cur_pos[0]][cur_pos[1]] != 'E':
        visited_stack.append(cur_pos)
        maze[cur_pos[0]][cur_pos[1]] = char
        mz.print()
        neighbors = mz.get_neighbors_solver(cur_pos)

        if neighbors:
            random_neighbor = random.choice(neighbors)
            cur_pos = random_neighbor[1]
        else:
            cur_pos = visited_stack.pop(-1)
    maze[cur_pos[0]][cur_pos[1]] = '&'

def dijkstras_maze_visualizer(mz):
    maze = mz.maze
    cur_pos = mz.get_start_pos()
    char = '&'
    distances = {}
    distances[cur_pos] = 0
    frontier = [cur_pos]
    while frontier:
        new_frontier = []
        for cell in frontier:
            neighbors = mz.get_neighbors_solver(cell)
            for linked in neighbors:
                if linked[1] not in distances:
                    distances[linked[1]] = distances[cell] + 1
                    new_frontier.append(linked[1])
            frontier = new_frontier
    temp_maze = maze.copy()
    for k,v in distances.items():
        temp_maze[k[0]][k[1]] = v
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if (r, c) in distances and maze[r][c] not in ['S', 'E']:
                maze[r][c] = str(distances[(r, c)] % 10)
    for row in maze:
        print(' '.join(row))

def main():
    maze = Maze(10,10)
    recursive_backtracking_map_generation(maze)
    maze.print()
    recursive_backtracking_maze_solver(maze)

if __name__ == '__main__':
    main()