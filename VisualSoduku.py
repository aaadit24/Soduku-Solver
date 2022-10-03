import pygame
from SudokuSolver import IsValid, IsEmpty
pygame.font.init()


class Grid:
    board = [
            [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]

    def __init__(self, size, window):
        self.rows_columns = 9
        self.cubes = [[Cube(self.board[i][j], i, j, size)
                       for j in range(9)] for i in range(9)]
        self.size = size
        self.model = None
        self.update_model()
        self.selected = None
        self.window = window

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.rows_columns)] for i in range(self.rows_columns)]

    def draw(self):
        # Draw Grid Lines
        gap = self.size / 9
        for i in range(self.rows_columns+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.window, (0, 0, 0),
                             (0, i*gap), (self.size, i*gap), thick)
            pygame.draw.line(self.window, (0, 0, 0),
                             (i * gap, 0), (i * gap, self.size), thick)

        # Draw Cubes
        for i in range(self.rows_columns):
            for j in range(self.rows_columns):
                self.cubes[i][j].draw(self.window)

    def solve_gui(self):
        self.update_model()
        find = IsEmpty(self.model)
        if not find:
            return True
        else:
            row, column = find

        for i in range(1, 10):
            if IsValid(self.model, row, column, i):
                self.model[row][column] = i
                self.cubes[row][column].set(i)
                self.cubes[row][column].draw_change(self.window, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(20)

                if self.solve_gui():
                    return True

                self.model[row][column] = 0
                self.cubes[row][column].set(0)
                self.update_model()
                self.cubes[row][column].draw_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(20)

        return False


class Cube:
    rows = 9
    columns = 9

    def __init__(self, value, row, column, size):
        self.value = value
        self.temp = 0
        self.row = row
        self.column = column
        self.size = size
        self.selected = False

    def draw(self, window):
        fnt = pygame.font.SysFont("cambri", 40)

        gap = self.size / 9
        x = self.column * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            window.blit(text, (x+5, y+5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (gap/2 - text.get_width()/2),
                               y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, window, g=True):
        fnt = pygame.font.SysFont("cambri", 40)

        gap = self.size / 9
        x = self.column * gap
        y = self.row * gap

        pygame.draw.rect(window, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        window.blit(text, (x + (gap / 2 - text.get_width() / 2),
                           y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(window, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val


def main():
    SIZE = 540
    window = pygame.display.set_mode((SIZE, SIZE))
    board = Grid(SIZE, window)
    window.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku Solver")
    board.draw()
    pygame.display.update()
    board.solve_gui()


main()
pygame.quit()
