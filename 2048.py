import random
import curses
from copy import deepcopy


class Board:
    def __init__(self, squareSize=10):
        self.tiles = [[None, None, None, None] for _ in range(4)]
        self.squareSize = squareSize
        self.ratioWH = .4
        self.score = 0

    def print(self):
        print("{}".format("-" * (4 * self.squareSize + 1)))
        for row in self.tiles:
            for _ in range(int((self.squareSize // 2) * self.ratioWH)):
                print("|{}".format("{}|".format(" " * (self.squareSize - 1)) * 4))
            for tile in row:
                if tile is None:
                    print("|{}".format(" " * (self.squareSize - 1)), end="")
                else:
                    print(("|{:^" + str(self.squareSize - 1) + "d}").format(tile), end="")
            print("|")
            for _ in range(int((self.squareSize // 2) * self.ratioWH)):
                print("|{}".format("{}|".format(" " * (self.squareSize - 1)) * 4))
            print("{}".format("-" * (4 * self.squareSize + 1)))

    def step(self):
        if self.isFilled():
            return
        while True:
            x, y = random.randint(0, 3), random.randint(0, 3)
            if self.tiles[x][y] is None:
                break
        if random.randint(0, 10) == 0:
            newTile = 4
        else:
            newTile = 2
        self.tiles[x][y] = newTile

    def isFilled(self):
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    return False
        return True

    def play(self):
        self.step()
        self.step()
        if __name__ == "__main__":
            printBoard(self)
        while True:
            if self.isLost() and __name__ == "__main__":
                global scoreBox
                scoreBox.addstr(2, 0, "You lose :(")
                scoreBox.refresh()
                return
            direction = getchar()
            isValidMove = False
            if direction == curses.KEY_LEFT:
                isValidMove = self.moveLeft()
            elif direction == curses.KEY_DOWN:
                isValidMove = self.moveDown()
            elif direction == curses.KEY_UP:
                isValidMove = self.moveUp()
            elif direction == curses.KEY_RIGHT:
                isValidMove = self.moveRight()
            elif direction == 113:
                return
            if isValidMove:
                self.step()
                if __name__ == "__main__":
                    printBoard(self)

    def isLost(self):
        temp = deepcopy(self.tiles)
        if self.moveLeft():
            self.tiles = temp
            return False
        elif self.moveUp():
            self.tiles = temp
            return False
        elif self.moveDown():
            self.tiles = temp
            return False
        elif self.moveRight():
            self.tiles = temp
            return False
        return True

    def moveLeft(self):
        modified = False
        for row in self.tiles:
            modified = self.collapse(row) or modified
        return modified

    def moveDown(self):
        self.tiles = self.rot90(self.tiles)
        modified = self.moveLeft()
        self.tiles = self.rot90(self.tiles)
        self.tiles = self.rot90(self.tiles)
        self.tiles = self.rot90(self.tiles)
        return modified

    def moveRight(self):
        self.tiles = self.rot90(self.tiles)
        self.tiles = self.rot90(self.tiles)
        modified = self.moveLeft()
        self.tiles = self.rot90(self.tiles)
        self.tiles = self.rot90(self.tiles)
        return modified

    def moveUp(self):
        self.tiles = self.rot90(self.tiles)
        self.tiles = self.rot90(self.tiles)
        self.tiles = self.rot90(self.tiles)
        modified = self.moveLeft()
        self.tiles = self.rot90(self.tiles)
        return modified

    def rot90(self, tiles):
        return list([list(x) for x in zip(*tiles[::-1])])

    def collapse(self, row):
        ret = self.compress(row)
        ret = self.merge(row) or ret
        return ret

    def compress(self, row):
        modified = False
        for i in range(len(row) - 1):
            for _ in range(4):
                if row[i] is None:
                    for j in range(i, len(row) - 1):
                        if row[j] != row[j + 1]:
                            modified = True
                        row[j] = row[j + 1]
                    row[-1] = None
        return modified

    def merge(self, row):
        modified = False
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and row[i] is not None:
                modified = True
                row[i] *= 2
                self.score += row[i]
                for j in range(i + 1, len(row) - 1):
                    row[j] = row[j + 1]
                row[-1] = None
        return modified


ratioWH = .5
mainScreen = None
cells = []
scoreBox = None


def getchar():
    return mainScreen.getch()


def main(stdscr):
    global mainScreen
    mainScreen = stdscr
    initBoard(stdscr)
    b = Board()
    b.play()
    if b.isLost() is not True:
        return
    while getchar() != 113:
        pass


def printBoard(b):
    for i in range(4):
        for j in range(4):
            cells[i][j].clear()
            cells[i][j].bkgd(curses.color_pair(0))
            if b.tiles[i][j] is None:
                pass
            else:
                if b.tiles[i][j] in colorsDict.keys():
                    cells[i][j].bkgd(curses.color_pair(colorsDict[b.tiles[i][j]]))
                cells[i][j].addstr(3, 6, str(b.tiles[i][j]))
            cells[i][j].border()
            cells[i][j].noutrefresh()
    scoreBox.addstr(1, 0, "{}".format(b.score))
    scoreBox.noutrefresh()
    curses.doupdate()


colorsDict = {
    2 ** 13: 13,
    2 ** 12: 12,
    2 ** 11: 11,
    2 ** 10: 10,
    2 ** 9: 9,
    2 ** 8: 8,
    2 ** 7: 7,
    2 ** 6: 6,
    2 ** 5: 5,
    2 ** 4: 4,
    2 ** 3: 3,
    2 ** 2: 2,
    2 ** 1: 1
}


def initColors():
    # Define new color constants
    lightRed = 8
    lightGreen = 9
    lightYellow = 10
    lightBlue = 11
    lightMagenta = 12
    lightCyan = 13
    lightWhite = 14

    # Define nonstandard colors
    i = 680
    curses.init_color(lightRed, i, i, i)
    curses.init_color(lightGreen, 0, i, 0)
    curses.init_color(lightYellow, i, i, 0)
    curses.init_color(lightBlue, 0, 0, i)
    curses.init_color(lightMagenta, i, 0, i)
    curses.init_color(lightCyan, 0, i, i)
    curses.init_color(lightWhite, i, i, i)

    # Init color pairs
    curses.init_pair(1, curses.COLOR_BLACK, lightRed)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, lightGreen)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, lightYellow)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(7, curses.COLOR_BLACK, lightBlue)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(9, curses.COLOR_BLACK, lightMagenta)
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(11, curses.COLOR_BLACK, lightCyan)
    curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(13, curses.COLOR_BLACK, lightWhite)
    curses.init_pair(14, curses.COLOR_BLACK, curses.COLOR_WHITE)


def initBoard(stdscr):
    # Tell user how to exit
    stdscr.addstr("Press q to exit")

    # Set curses options
    curses.noecho()
    curses.cbreak()

    # Initialize colors
    initColors()

    # Initialize game windows
    mainBox = curses.newwin(int(84 * ratioWH), 82, int(12 * ratioWH), 20)
    mainBox.box()
    stdscr.noutrefresh()
    mainBox.noutrefresh()
    global cells
    for i in range(4):
        row = []
        cells.append(row)
        for j in range(4):
            cell = mainBox.derwin(int(16 * ratioWH), 16, int((5 + 20 * i) * ratioWH), 3 + 20 * j)
            cell.border()
            cell.noutrefresh()
            row.append(cell)

    # Initialize score window
    global scoreBox
    scoreBox = curses.newwin(int(20 * ratioWH), 20, 20, 130)
    scoreBox.addstr("Score:")
    scoreBox.noutrefresh()

    # Finally, refresh the screen
    curses.doupdate()


if __name__ == "__main__":
    curses.wrapper(main)
