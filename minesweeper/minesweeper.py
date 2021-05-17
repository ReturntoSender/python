import pygame as pg
from dataclasses import dataclass
import random as rnd


resolution = 400
grid = 20
size = resolution // grid
mine_count = 20

pg.init()
screen = pg.display.set_mode([resolution, resolution])
cell_normal = pg.transform.scale(
    pg.image.load("Teil_10_ms_cell_normal.gif"), (size, size)
)
cell_marked = pg.transform.scale(
    pg.image.load("Teil_10_ms_cell_marked.gif"), (size, size)
)
cell_mine = pg.transform.scale(pg.image.load("Teil_10_ms_cell_mine.gif"), (size, size))
cell_selected = []
for n in range(9):
    cell_selected.append(
        pg.transform.scale(pg.image.load(f"Teil_10_ms_cell_{n}.gif"), (size, size))
    )

matrix = []
next_cells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class Cell:
    row: int
    column: int
    mine: bool = False
    selected: bool = False
    flagged: bool = False
    next_to = int = 0

    def show(self):
        pos = (self.column * size, self.row * size)
        if self.selected:
            if self.mine:
                screen.blit(cell_mine, pos)
            else:
                screen.blit(cell_selected[self.next_to], pos)
        else:
            if self.flagged:
                screen.blit(cell_marked, pos)
            else:
                screen.blit(cell_normal, pos)

    def count_mines_next(self):
        for pos in next_cells:
            new_row = self.row + pos[0]
            new_column = self.column + pos[1]
            if (
                new_row >= 0
                and new_row < grid
                and new_column >= 0
                and new_column < grid
            ):
                if matrix[new_row * grid + new_column].mine:
                    self.next_to += 1


def floodfill(row, column):
    for pos in next_cells:
        new_row = row + pos[0]
        new_column = column + pos[1]
        if new_row >= 0 and new_row < grid and new_column >= 0 and new_column < grid:
            cell = matrix[new_row * grid + new_column]
            if cell.next_to == 0 and not cell.selected:
                cell.selected = True
                floodfill(new_row, new_column)
            else:
                cell.selected = True


for n in range(grid * grid):
    matrix.append(Cell(n // grid, n % grid))

while mine_count > 0:
    x = rnd.randrange(grid * grid)
    if not matrix[x].mine:
        matrix[x].mine = True
        mine_count -= 1

for object in matrix:
    object.count_mines_next()

go_on = True
while go_on:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            go_on = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseX, mouseY = pg.mouse.get_pos()
            column = mouseX // size
            row = mouseY // size
            i = row * grid + column
            cell = matrix[i]
            if pg.mouse.get_pressed()[2]:
                cell.flagged = not cell.flagged
            if pg.mouse.get_pressed()[0]:
                cell.selected = True
                if cell.next_to == 0 and not cell.mine:
                    floodfill(row, column)
                if cell.mine:
                    for object in matrix:
                        object.selected = True
    for object in matrix:
        object.show()
    pg.display.flip()

pg.quit()
