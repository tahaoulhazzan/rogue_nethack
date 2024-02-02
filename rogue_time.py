import curses
import random
import time

class Character:
    def __init__(self, stdscr):
        self.x = 1
        self.y = 1
        self.stdscr = stdscr
        self.run = True

    def move(self, dungeon_map, enemy):
        key = self.stdscr.getch()
        new_x, new_y = self.x, self.y

        if key == ord('q'):
            self.run = False
        elif key == ord('e') and self.y > 1:
            new_y -= 1
        elif key == ord('x'):
            new_y += 1
        elif key == ord('d'):
            new_x += 1
        elif key == ord('s') and self.x > 1:
            new_x -= 1

        if dungeon_map[new_y][new_x] in '.,+,=,#' and (new_x, new_y) != (enemy.x, enemy.y):
            self.x, self.y = new_x, new_y

class Enemy:
    def __init__(self, stdscr, x, y):
        self.x = x
        self.y = y
        self.stdscr = stdscr

    def move_towards(self, target_x, target_y):
        # Move towards the target (player)
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

    def move(self, dungeon_map, player):
        # Move towards the player's position
        self.move_towards(player.x, player.y)

class Dungeon:
    def __init__(self, stdscr):
        self.map = [
            "__________        __________",
            "|........|        |........|",
            "|........|  ######+........|",
            "|........+###     |........|",
            "__________  #     ____+_____",
            "            #         #     ",
            "            ###########     ",
            "              #             ",
            "          ____+____         ",
            "          |.......|         ",
            "          |.......|         ",
            "          _________         "
        ]
        self.player = Character(stdscr)
        self.enemy = Enemy(stdscr, 5, 3)  # Example enemy starting position
        self.last_enemy_move_time = time.time()

    def display(self):
        self.player.stdscr.clear()
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                self.player.stdscr.addch(y, x, tile)
        self.player.stdscr.addch(self.player.y, self.player.x, '@')
        self.player.stdscr.addch(self.enemy.y, self.enemy.x, 'E')  # Display the enemy

    def gain(self):
        pass

def main(stdscr):
    dungeon = Dungeon(stdscr)
    while dungeon.player.run:
        dungeon.display()
        dungeon.player.move(dungeon.map, dungeon.enemy)

        # Move the enemy every 1 second
        current_time = time.time()
        if current_time - dungeon.last_enemy_move_time >= 1:
            dungeon.enemy.move(dungeon.map, dungeon.player)
            dungeon.last_enemy_move_time = current_time

        time.sleep(0.1)  # Slow down the game loop for a more visible effect

if __name__ == "__main__":
    curses.wrapper(main)
