
import curses

class Character:
    def __init__(self, stdscr):
        self.x = 1
        self.y = 1
        self.stdscr = stdscr
        self.run = True

    def move(self):
        key = self.stdscr.getch()
        if key == ord('q'):
            self.run = False
        elif key == curses.KEY_UP and self.y > 1:
            self.y -= 1
        elif key == curses.KEY_DOWN:
            self.y += 1
        elif key == curses.KEY_RIGHT:
            self.x += 1
        elif key == curses.KEY_LEFT and self.x > 1:
            self.x -= 1

class Dungeon:
    def __init__(self, stdscr):
        self.map = [
            "##########",
            "#........#",
            "#+.......#",
            "#........#",
            "##########",
        ]
        self.player = Character(stdscr)

    def display(self):
        self.player.stdscr.clear()
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                self.player.stdscr.addch(y, x, tile)
        self.player.stdscr.addch(self.player.y, self.player.x, '@')

def main(stdscr):
    dungeon = Dungeon(stdscr)
    while dungeon.player.run:
        dungeon.display()
        dungeon.player.move()

if __name__ == "__main__":
    curses.wrapper(main)
