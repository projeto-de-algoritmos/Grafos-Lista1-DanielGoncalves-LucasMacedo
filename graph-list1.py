import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (139, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 139)
YELLOW = (222, 178, 0)

BORDER_THICKNESS = 1.0

WIDTH = 600
HEIGHT = 600
SCREEN_SIZE = (WIDTH, HEIGHT)

POS_X_INIT = 0
POS_Y_INIT = 0

SIZE = 20
CLOCK = pygame.time.Clock()

class NodeBorder():
    def __init__(self, pos_x, pos_y, width, height):
        self.color = BLACK
        self.thickness = BORDER_THICKNESS
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])


class Node():
    def __init__(self, pos_x, pos_y):
        self.color = BLUE

        self.visited = False

        self.matrix_pos_x = 0
        self.matrix_pos_y = 0

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = SIZE
        self.height = SIZE

        self.top_border = NodeBorder(self.pos_x, self.pos_y, SIZE, BORDER_THICKNESS)
        self.bottom_border = NodeBorder(self.pos_x, self.pos_y + SIZE - BORDER_THICKNESS, SIZE, BORDER_THICKNESS)
        self.right_border = NodeBorder(self.pos_x + SIZE - BORDER_THICKNESS, self.pos_y, BORDER_THICKNESS, SIZE)
        self.left_border = NodeBorder(self.pos_x, self.pos_y, BORDER_THICKNESS, SIZE)

        self.neighbors = []

        self.neighbors_connected = []

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])

        self.top_border.render(background)
        self.bottom_border.render(background)
        self.right_border.render(background)
        self.left_border.render(background)

class Maze():
    def __init__(self):
        self.maze = []
        self.total_nodes = 0
        x = 0
        y = 0

        for i in range(0, WIDTH, SIZE):
            self.maze.append([])
            for j in range(0, HEIGHT, SIZE):
                self.maze[x].append(Node(i , j))
                self.total_nodes += 1
                y += 1
            x += 1

        self.define_neighbors()

    def add_edge(self, node, neighbor):
        neighbor.neighbors_connected.append(node)
        node.neighbors_connected.append(neighbor)

    def remove_neighbors_visited(self, node):
        node.neighbors = [x for x in node.neighbors if not x.visited]
 
    def define_neighbors(self):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].matrix_pos_x = i
                self.maze[i][j].matrix_pos_y = j
                if i > 0 and j > 0 and i < int(HEIGHT / SIZE) - 1 and j < int(HEIGHT / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bot
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1]) # left
                elif i == 0 and j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bot
                elif i == int(HEIGHT / SIZE) - 1 and j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1]) # right
                elif i == 0 and j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1]) # left
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bot
                elif i == int(HEIGHT / SIZE) - 1 and j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1]) # left
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j]) # top
                elif j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bot
                elif i == 0:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bot
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1]) # left
                elif i == int(HEIGHT / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1]) # left
                elif j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bot
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1]) # left
            print('[NEIGHBORS ' + str(len(self.maze[i][j].neighbors)) + ']')

    def break_border(self, node, neightbor, color):
        # right
        if (neightbor.matrix_pos_x == node.matrix_pos_x + 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.right_border.color = color
            neightbor.left_border.color = color
        # left
        elif (neightbor.matrix_pos_x == node.matrix_pos_x - 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.left_border.color = color
            neightbor.right_border.color = color
        # bot
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y + 1):
            node.bottom_border.color = color
            neightbor.top_border.color = color
        # top
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y - 1):
            node.top_border.color = color
            neightbor.bottom_border.color = color
    
    def dfs(self):
        current_cell = random.choice(random.choice(self.maze))
        current_cell.visited = True
        current_cell.color = GREEN
        stack = [current_cell]
        visited_cells = 1
        
        print('[POS X MATRIX ' + str(current_cell.matrix_pos_x) + ']')
        print('[POS Y MATRIX ' + str(current_cell.matrix_pos_y) + ']')
        print('[NEIGHBORS ' + str(len(current_cell.neighbors)) + ']')

        while visited_cells != self.total_nodes or len(stack) != 0:
            print('[TOTAL NODES ' + str(self.total_nodes) + ']')
            print('[VISITED NODES ' + str(visited_cells) + ']')
            print('[STACK ' + str(len(stack)) + ']')
            print('[NEIGHBORS ' + str(len(current_cell.neighbors)) + ']')
            
            self.remove_neighbors_visited(current_cell)
            if len(current_cell.neighbors) > 0:
                random_neighbor = random.choice(current_cell.neighbors)

                self.break_border(current_cell, random_neighbor, YELLOW)

                self.add_edge(current_cell, random_neighbor)
                current_cell = random_neighbor
                stack.append(current_cell)
                current_cell.visited = True
                current_cell.color = GREEN
                visited_cells += 1
            else:
                current_cell.color = YELLOW
                if len(stack) == 1:
                    stack.pop()
                else:
                    stack.pop()
                    current_cell = stack[-1]
                    
    def render(self, background):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].render(background)

class Player():
    def __init__(self):
        self.pos_x = POS_X_INIT + BORDER_THICKNESS
        self.pos_y = POS_Y_INIT + BORDER_THICKNESS
        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS
        self.color = RED

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.pos_x > BORDER_THICKNESS:
                    self.pos_x -= SIZE
                if event.key == pygame.K_RIGHT and self.pos_x + BORDER_THICKNESS < WIDTH - SIZE:
                    self.pos_x += SIZE
                if event.key == pygame.K_UP and self.pos_y > BORDER_THICKNESS: 
                    self.pos_y -= SIZE
                if event.key == pygame.K_DOWN and self.pos_y + BORDER_THICKNESS < HEIGHT - SIZE:
                    self.pos_y += SIZE

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])

class Game():
    def __init__(self):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')

        self.exit = False

    def load(self):
        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Maze Game')
        self.maze = Maze()
        self.maze.dfs()
        self.player = Player()
        
                
    def unload(self):
        pass

    def update(self):
        self.player.update()

    def render(self):
        self.background.fill(BLACK)
        
        self.maze.render(self.background)

        self.player.render(self.background)
        pygame.display.update()

    def run(self):
        self.load()

        while not self.exit:
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.exit = True

            self.update()
            self.render()
        
        pygame.quit()
        
def main():
    mygame = Game()
    mygame.run()

if __name__ == '__main__':
    main()