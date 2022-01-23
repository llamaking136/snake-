# no u don't steal my codez :((((
# by llamaking136, under some kind of licence
# i forgor :O

import sys
if sys.version_info.major <= 2:
    print("Sorry, you need Python 3+ to use this game. :(")
    sys.exit(1)

try:
    import pygame
    from pygame.locals import *
    from loguru import logger
    import time
    import enum
except ImportError:
    try:
        import pip
    except ImportError:
        raise ImportError("Plz install pip and re-run script")
        exit(2)
    old_argv = sys.argv
    sys.argv = ["pip", "install", "pygame", "loguru"]
    pip.main()
    sys.argv = old_argv
    del pip, old_argv
    print("Packages installed, please re-run")
    exit(0)

pygame.init()
pygame.font.init()

TITLE = "Snake But With Two Snakes Instead Of One"

WIDTH = 600
HEIGHT = 600

DOWN_KEYS = {}

SCREEN = pygame.display
SURFACE = SCREEN.set_mode((WIDTH, HEIGHT))

FramePerSec = pygame.time.Clock()
FPS = 15

def getkeydown(key):
    try:
        if DOWN_KEYS[ord(key)]:
            return True
        else:
            return False
    except KeyError:
        return False

class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.x = [None for _ in range(width)]
        # self.y = [None for _ in range(height)]
        self.arr = [[None for _ in range(y)] for _ in range(x)]

class Snake:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.length = 1
        self.isDead = False
        self.direction = Direction.RIGHT
        self.boxes = [(x, y), (x - 1, y)]

        self.grid.arr[x][y] = True
    
    def eat(self): # TODO: FINISH
        self.length += 1
        # get last boxes' position and set the new box back one position
        lastbox = self.boxes[-1]
        if lastbox[0] == 0 or lastbox[0] == self.grid.width - 1: # if at the left edge or at the right edge
            newpos = [0, lastbox[1] + 1]

    def getDirection(self, direction, coord):
        if direction == Direction.UP:
            return (coord[0], coord[1] + 1)
        elif direction == Direction.DOWN:
            return (coord[0], coord[1] - 1)
        elif direction == Direction.LEFT:
            return (coord[0] - 1, coord[1])
        elif direction == Direction.RIGHT:
            return (coord[0] + 1, coord[1])

    def update(self):
        index = 0
        for i in self.boxes:
            old_i = i
            coord = self.getDirection(self.direction, i)
            # turn the last box from on to off
            self.grid.arr[coord[0]][coord[1]] = True
            self.grid.arr[old_i[0]][old_i[1]] = None
            self.boxes[index] = coord

            index += 1

BOX_NUM_X  = 60
BOX_NUM_Y  = 60
BOX_WIDTH  = WIDTH  / BOX_NUM_X
BOX_HEIGHT = HEIGHT / BOX_NUM_Y

grid = Grid(BOX_NUM_X, BOX_NUM_Y)
snake = Snake(1, BOX_NUM_Y // 2, grid)

snake1_color = (0, 255, 0)
snake2_color = (0, 0, 255)

@logger.catch
def main():
    x = 0
    y = HEIGHT // 2

    sleep_time = 500
    time_until_sleep = 0 # millisecond when we stop sleeping
    do_update = True

    prev_time = 0
    dt = 0
    rev = False

    while True:
        t = pygame.time.get_ticks()

        dt = (t - prev_time) / 1000
        prev_time = t

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                DOWN_KEYS[event.key] = True
            if event.type == KEYUP:
                DOWN_KEYS[event.key] = False

        # do stuff...
        SCREEN.set_caption(TITLE + " | " + str(round(FramePerSec.get_fps(), 2)) + " FPS")

        SURFACE.fill((0, 0, 0))

        if do_update:
            snake.update()
            do_update = False
            time_until_sleep = t + sleep_time
        grid = snake.grid
        for i in snake.boxes:
            pygame.draw.rect(SURFACE, snake1_color, (i[0] * BOX_WIDTH, i[1] * BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT))

        if not do_update:
            if t >= time_until_sleep:
                do_update = True

        pygame.display.flip()
        
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()
