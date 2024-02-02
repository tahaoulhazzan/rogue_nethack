from random import randint

def create_grille(n, m, nbgold):
    grille = [[0 for _ in range(n)] for _ in range(n)]
    donjon = randint(3, 5)

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

                path_end = (x + l // 2, y)
                I[path_end[0]][path_end[1]] = 4

                for p in range(path_start[0], path_end[0] + 1):
                     I[p][path_start[1]] = 5

                for q in range(path_start[1], path_end[1] + 1):
                     I[path_end[0]][q] = 5


    perso=randint(1,donjon)
    (i,j)=M[perso-1]
    (l,c)=L[perso-1]
    I[i+l//2][j+c//2]="@"
    for k in range(m):
        mechant=randint(0,donjon-1)
        (i,j)=M[mechant]
        (l,c)=L[mechant]
        abs=randint(0,l-1)
        ord=randint(0,c-1)
        I[i+abs][l+ord]="m"
        

    return I

          

            
          

# Example usage:
n = 50
nbméchants = 3
nbgold = 2
resulting_grille = create_grille(n, nbméchants, nbgold)
for row in resulting_grille:  
     print(row)
     

    


            
                
    
      


