import pygame
import time
import main as m

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)


class Grid:
    board = [
            [8, 0, 2, 0, 0, 6, 0, 5, 0],
            [0, 4, 0, 0, 1, 8, 0, 0, 0],
            [0, 9, 0, 0, 0, 3, 0, 8, 4],
            [2, 0, 0, 0, 0, 9, 8, 0, 1],
            [0, 1, 0, 0, 0, 0, 5, 4, 9],
            [0, 8, 0, 0, 3, 0, 6, 0, 0],
            [0, 7, 8, 9, 0, 2, 4, 0, 5],
            [0, 2, 9, 0, 0, 5, 7, 0, 3],
            [5, 0, 1, 0, 7, 0, 9, 0, 8]
        ]
    
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(i, j, self.board[j][i], width, height) for j in range(rows)] for i in range(cols)]
        self.width = width
        self.height = height
        self.mod = None
        self.selected = None

    def model(self):
        #to update a model to check if inputs are valid
        self.mod = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def place(self, value):
        #check if places where values entered are valid using solver methods from main class
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_val(value)
            self.model()

            if m.isValid(self.mod, value, row, col) and m.solve(self.mod):
                return True
            else:
                self.cubes[row][col].set_val(0)
                self.cubes[row][col].set_temp(0)              
                self.model()
                return False

    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
        
    def guess(self, key):
        #set temp values based on guesses
        row, col = self.selected
        self.cubes[row][col].set_temp(key)


    def click(self, pos):
        # get position in terms of row and col based on mouse click
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(x), int(y))
        else:
            return None

    def clear(self):
        #clear entered value when backspace is pressed
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def select(self, row, col):
        #identify selected pos
        for i in range(self.rows):
            for j in range(self.cols):
                #other cubes are now false since they weren't selected
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)
    
    def is_finished(self):
        #check if board is finished
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, row, col, value, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    def set_temp(self, temp):
        self.temp = temp
    def set_val(self, value):
        self.value = value


    def draw(self, win):
        #Gap b/c the width and height of cube is the width and height of the grid, so you have to scale it down for each cube
        gap = self.width/9
        x = self.row * gap
        y = self.col * gap
        #(x, y, gap, gap) --> left, top, width, height
        pygame.draw.rect(win, BLACK, (x, y, gap, gap), 3)
        if self.value != 0:
            font = pygame.font.SysFont('comicsans', 30)
            txt = font.render(str(self.value), 20, BLACK)
            win.blit(txt, (x+15, y+15))
        elif self.temp != 0 and self.value == 0:
            font = pygame.font.SysFont('comicsans', 30)
            txt = font.render(str(self.temp), 20, BLACK)
            win.blit(txt, (x+15, y+15))
        if self.selected:
            font = pygame.font.SysFont('comicsans', 30)
            txt = font.render(str(self.temp), 20, GRAY)
            win.blit(txt, (x+15, y+15))

def time_format(win, start):
    mins = start // 60
    secs = start % 60
    hour = mins // 60
    return "  " + str(mins) + ":" + str(secs)

def redraw(win, board, start):
    win.fill(WHITE)
    text = time_format(win, start)
    font = pygame.font.SysFont('comicsans', 30)
    txt = font.render("Time: " + text, 1, BLACK)
    win.blit(txt, (375, 560))
    board.draw(win)
    
def main():
    WIN = pygame.display.set_mode((540, 600))
    run = True
    key = None
    #for the time
    start = time.time()
    board = Grid(9, 9, 540, 540)
    pygame.display.set_caption('Sudoku')
    while run:
        #get time since start of playing
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            #keys pressed
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                #check if valid entry
                if event.key == pygame.K_RETURN:
                    row, col = board.selected
                    #check if anything is entered in selected cube
                    if board.cubes[row][col].temp != 0:
                        if board.place(board.cubes[row][col].temp):
                            print('Correct')
                        else:
                            print('Incorrect')
                        key = None
                    if board.is_finished():
                        print('Completed')
                        run = False
            
            #get pos based on mouseclick
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        if board.selected and key != None:
            board.guess(key)

        #always redraw and update
        redraw(WIN, board, play_time)
        pygame.display.update()

main()
pygame.quit()