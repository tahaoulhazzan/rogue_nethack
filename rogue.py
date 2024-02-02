import curses
import random
import time
import numpy as np

class Character:
    def __init__(self, stdscr):
        self.x = 1
        self.y = 1
        self.stdscr = stdscr
        self.run = True

    def move(self, dungeon_map, enemy):
        key = None
        self.stdscr.timeout(1000)  # Attendre 1 seconde sans bloquer l'entrée utilisateur
        try:
            key = self.stdscr.getch()
        except curses.error:
            pass  # En cas d'erreur, par exemple si la fenêtre est redimensionnée
        finally:
            self.stdscr.timeout(-1)  # Réinitialiser le timeout à l'infini

        if key == ord('q'):
            self.run = False
        elif key is not None:  # Si une touche a été pressée
            new_x, new_y = self.x, self.y
            if key == ord('e') and self.y > 1:
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
        

    def move_towards(self,dungeon_map, target_x, target_y,player):
        # Move towards the target (player)
        #if player and enemy in same room :

                
            X=(target_x-self.x)
            Y=(target_y-self.y)
            if np.abs(X)>=np.abs(Y) :
                new_x=self.x+int(X/(np.abs(X)))
                if dungeon_map[self.y][new_x] in '.,+,=,#' and (new_x, self.y) != (player.x, player.y):
                    self.x=new_x
            else :
                new_y=self.y+int(Y/(np.abs(Y)))
                if dungeon_map[new_y][self.x] in '.,+,=,#' and (self.x, new_y) != (player.x, player.y):
                    self.y=new_y
        #else :
                #get to the nearest door
            
    def move(self, dungeon_map, player):
        # Move towards the player's position
        self.move_towards(dungeon_map,player.x, player.y,player)

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

    from random import randint

from random import randint

def create_grille(n,):
    grille = [[0 for _ in range(n)] for _ in range(n)]
    donjon = randint(3, 6)
    E=[]
    X=[[] for _ in range(donjon)]

    # La taille de la grille vaut n^2 et on a entre 3 et 5 donjons
    # On décide que la surface avec celles des donjons doit être égale à la moitié de la surface totale
    s = n * n // 1.5
    L = []
    surface = 0

    # Générer les dimensions des donjons
    for j in range(donjon):
        l = randint(4, 10)
        c = randint(4, 10)
        L.append((l, c))
        surface += l * c

    # Si la surface dépasse s, régénérer les dimensions des donjons
    while surface > s:
        L = []
        surface = 0
        for j in range(donjon):
            l = randint(4, 10)
            c = randint(4, 10)
            L.append((l, c))
            surface += l * c
   

    # On veut générer aléatoirement la position en haut à droite des grilles
    I = [[0 for _ in range(n)] for _ in range(n)]
    M = []

    for j in range(donjon):
        P=[]
        (l, c) = L[j]
        r = True

        while r:
            K = [row[:] for row in I]  
            r = False
            x = randint(1, n - 1 - l)
            y = randint(1, n - 1 - c)
            M.append((x, y))

            for i in range(l):
                for k in range(c):
                    if K[x + i][y + k] != 0:
                        r = True

                    K[x + i][y + k] = 1

            I = [row[:] for row in K] 
           # Ajouter les murs autour des donjons
            for i in range(1, l - 1):
                I[x + i][y] = 2
                I[x + i][y + c] = 2

            for k in range(c):
                I[x][y + k] = 3
                I[x + l][y + k] = 3
             # Ajouter des chemins (4) entre deux donjons
            if j > 0:
                (prev_x, prev_y) = M[j - 1]
                path_start = (prev_x + L[j - 1][0] // 2, prev_y + L[j - 1][1] - 1)
                I[path_start[0]][path_start[1]] = 4
                X[j-1].append(path_start)
                
                path_end = (x + l // 2, y)
                I[path_end[0]][path_end[1]] = 4
                X[j].append(path_end)
                for p in range(path_start[0], path_end[0] + 1):
                     I[p][path_start[1]] = 5

                for q in range(path_start[1], path_end[1] + 1):
                     I[path_end[0]][q] = 5
    for j in range(donjon):
         E.append([M[j],L[j],X[j]])

    perso=randint(1,donjon)
    (i,j)=M[perso-1]
    (l,c)=L[perso-1]
    I[i+l//2][j+c//2]="@"
   ## for k in range(m):
   ##     mechant=randint(0,donjon-1)
   ##     (i,j)=M[mechant]
   ##     (l,c)=L[mechant]
   ##     abs=randint(0,l-1)
   ##     ord=randint(0,c-1)
   ##     I[i+abs][j+ord]="m"
   ##    for k in range(nbgold):
   ##     place=randint(0,donjon-1)
   ##     (i,j)=M[place]
   ##     (l,c)=L[place]
   ##     abs=randint(1,l-1)
   ##     ord=randint(1,c-1)
   ##     while I[i+abs][j+ord]=="m":
   ##         place=randint(0,donjon-1)
   ##         (i,j)=M[place]
   ##         (l,c)=L[place]
   ##         abs=randint(1,l-1)
   ##         ord=randint(1,c-1)
   ##     I[i+abs][j+ord]="g"

        

    return donjon,I,E
    
          

# Example usage:
n = 50

resulting_grille = create_grille(n)
for row in resulting_grille:  
     print(row)

def matrice(carte):
     
    carte_terminal=[]

    for y in range(len(carte)):
        ligne=""
        for x in range(len(carte[0])):
            if carte[y][x]==3:
                ligne.append("-")

            elif carte[y][x]==1:
                ligne.append(".")

            elif carte[y][x]=='@':
                ligne.append("@")
            elif carte[y][x]=='m':
                ligne.append("S")
            elif carte[y][x]==4:
                ligne.append("+")
            elif carte[y][x]==5:
                ligne.append("#")

            elif carte[y][x]=='potion':

                ligne.append("j")

            elif carte[y][x]=='argent':
                ligne.append("*")

            elif carte[y][x]=='couteau':
                ligne.append("!")
            elif carte[y][x]=='arc':
                ligne.append(")")

            elif carte[y][x]=='armure':
                ligne.append("^")

            elif carte[y][x]==0:
                ligne.append("")
            elif carte[y][x]==2:
                ligne.append("|")

        chaine=''.join(ligne)
        carte_terminal.append(chaine)

