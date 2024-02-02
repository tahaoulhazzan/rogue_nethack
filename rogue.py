
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
        elif key == ord('e') and self.y > 1:
            self.y -= 1
        elif key == ord('x'):
            self.y += 1
        elif key == ord('d'):
            self.x += 1
        elif key == ord('s') and self.x > 1:
            self.x -= 1

class ennemy:
    def __init__(self,stdscr):
        self.ennemy_x=None
        self.ennemy_y=None

        


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

    def gain(self):
        pass

def main(stdscr):
    dungeon = Dungeon(stdscr)
    while dungeon.player.run:
        dungeon.display()
        dungeon.player.move()

if __name__ == "__main__":
    curses.wrapper(main)
