import numpy as np
import random as rnd
from Pieces import *
"----------------------------------------------------------------------------------------------------------------------"
class Puzzle:
    "Un puzzle est défini par:"
    "- pieces: La liste de toutes les pièces (de la classe Piece) du puzzle "
    "- size: un couple d'entiers correspondant aux dimensions du puzzle (hauteur, largeur). Celles-ci seront désignées par le couple (ha,la)"
    "- c: None pour un puzzle sans couleur, 1 pour un damier, 2 pour un dégradé"

    op = {}

    def __init__(self,pieces,size,c) :
         self.pieces=pieces
         self.size=size
         self.c=c

    def getsize(self):
        return(self.size)

    def getlistpieces(self):
        return (self.pieces)
    
    def getC(self):
        return self.c

    @staticmethod
    def ordreparcours(size):
        "Fonction qui prend en argument un couple d'entiers (les dimensions du puzzle)"
        "Renvoie la liste des couples (coordonnées) ordonnés dans l'ordre dans lequel un puzzle de cette dimension va être parcouru "
        "Rq: l'ordre de parcours est une convention."
        "Il consiste à parcourir les bords du puzzle dans le sens horaire en partant du coin HG puis en parcourant l'intérieur de la gauche vers la droite de haut en bas"
        if size in Puzzle.op:
            return Puzzle.op[size]
        l=[]
        (ha,la)=size
        for j in range(0,la):
            l.append((0,j))
        for i in range(1,ha):
            l.append((i,la-1))
        for j in range(la-2,-1,-1):
            l.append((ha-1,j))
        for i in range(ha-2,0,-1):
            l.append((i,0))
        for i in range(1,ha-1):
            for j in range(1,la-1):
                l.append((i,j))
        Puzzle.op[size]=l
        return l


def tourner_alea(L):
    "Fonction auxiliaire de cree_puzzle qui prend en argument une liste d'entiers"
    "Cette fonction 'tourne une pièce' ie permutte circulairement le bord de 0 à 3 quarts de tour aléatoirement"
    "Elle renvoie une liste correspondant à aux bords de la pièce tournée"
    tour=rnd.randint(0,4)
    M=[]
    for i in range (len(L)):
            M.append(L[((i-tour+len(L))%(len(L)))])
    return(M)

def cree_puzzle(ha,la,L,c=None):
    "Fonction qui prend en argument deux entiers correspondant aux dimensions du puzzle voulu et une liste correspondant aux types d'encoches possibles"
    "Crée un puzzle aléatoirement, solvable, aux dimensions et encoches souhaitées "
    "Renvoie un élement de la classe Puzzle"
    "Rq: le premier élement de la liste des pièces est la pièce d'identifiant 0 (permet d'avoir le puzzle à l'endroit pour le représenter)"
    puzzle=np.ndarray((ha,la),dtype=list)
    #on initialise le haut des pièces
    for i in range(ha):
        for j in range(la):
            if i==0:
                puzzle[0][j]=[0]
            else:
                puzzle[i][j]=[rnd.choice(L)]
    #on initialise les bords droits
    for i in range(ha):
        for j in range(la):
            if j==la-1:
                puzzle[i][j].append(0)
            else:
                puzzle[i][j].append(rnd.choice(L))
    #on initialise le bas des pièces
    for i in range (ha):
        for j in range(la):
            if i==ha-1:
                puzzle[i][j].append(0)
            else:
                puzzle[i][j].append(- puzzle[i+1][j][0])
    #on initialise les bords gauches
    for i in range(ha):
        for j in range(la):
            if j==0:
                puzzle[i][j].append(0)
            else:
                puzzle[i][j].append(- puzzle[i][j-1][1])
    #on crée la liste correspondant à la liste des pièces du puzzle en positionnant en première position la pièce d'identifiant 0 et en mélangeant le reste des pièces avec des rotations aléatoires"
    liste=[]
    identifiant=1
    for i in range(ha):
        for j in range(la):
            if i+j==0:
                if c==1 :
                    piece0=Piece(id=i+j,bord=puzzle[i][j],couleur=0)
                else :
                    piece0=Piece(id=i+j,bord=puzzle[i][j])
            else:
                liste.append(Piece(id=identifiant,bord=tourner_alea(puzzle[i][j])))
                if c==1 :
                    liste[identifiant-1].set_couleur((i+j)%2)
                identifiant+=1
    rnd.shuffle(liste)
    return(Puzzle(pieces=[piece0]+liste,size=(ha,la),c=c))






