from Puzzle import *
from Pieces import *

class Essai:
    "Un essai est défini par :"
    " - piece: sa pièce (de la classe Piece)"
    " - i,j : ses coordonneés (deux entiers correspondant au numéro de la ligne et au numéro de colonne)"
    " - rotation : sa rotation (un entier entre 0 et 3)"

    def __init__(self,piece,i,j,rotation):
        self.piece=piece
        self.coord=(i,j)
        self.rotation=rotation

    def getpiece(self):
        return(self.piece)

    def geti(self):
        return(self.coord[0])

    def getj(self):
        return(self.coord[1])

    def getrotation(self):
        return(self.rotation)


E0 = Essai(piece=Piece(id=-1, bord=[0, 0, 0, 0]), i=-1, j=-1, rotation=0)

class Etat:
    "Un état est défini par :"
    " - posees : matrice des essais posés (None là où il n'y en a pas encore) aux coordonnées qui leur sont associées. posees est donc une matrice d'essais"
    " - fail : matrice telle qu'aux coordonnées i,j se trouve une liste d'essais qui ont échoué pour cet endroit. fail est donc une matrice de listes d'essais "
    " - pieces_restantes : la liste des listes des pièces restantes rangées selon leur classe d'équivalence "

    def __init__(self,posees,fail,pieces_restantes):
        self.posees = posees
        self.fail = fail
        self.pieces_restantes=pieces_restantes

    def getPosees(self):
        return self.posees

    def getFail(self) :
        return self.fail
    
    def getPiecesrestantes(self) :
        return self.pieces_restantes
    
    def getlistfail(self,i,j):
        "Prend en argument les coordonnées i et j"
        "Renvoie la liste des essais qui ont échoué pour l'emplacement (i,j) ( la liste vide s'il n'y en a aucun)"
        if self.fail[i][j]==None:
            return([])
        else:
            return(self.fail[i][j])

    def getEssaipose(self,i,j):
        "Prend en argument les coordonnées i et j"
        "Renvoie l'essai qui a été posé en i et j, renvoie alors None s'il n'y en a pas"
        return(self.posees[i][j])

    def getlastEssai(self):
        "Renvoie l'essai qui a été posé en dernier dans l'ordre de parcours"
        m=self.getPosees()
        ordreparc=Puzzle.ordreparcours(m.shape)
        for k in range(len(ordreparc)):
            (x,y)=ordreparc[k]
            if m[x][y]==None:
                (i,j)=ordreparc[k-1]
                return(self.getEssaipose(i,j))

    def ranger_piece(self,p,liste):
        liste[p.getClasse()].append(p)

    def rangerfail(self,essai):
        "Prend un argument un essai"
        "Ajoute cet essai à la liste des ratés dans la matrice fail, au bon endroit "
        (i,j)=(essai.geti(),essai.getj())
        if self.fail[i][j] == None:
            self.fail[i][j] = [essai]
        else:
            if not (essai_in(essai,self.fail[i][j])) : #on vérifie que l'essai n'est pas déjà dans les fail"
                self.fail[i][j].append(essai)
        self.posees[i][j]=None #on retire l'essai des essais posés
        self.ranger_piece(essai.getpiece(),self.getPiecesrestantes()) #on rajoute la pièce correspondante aux pièces restantes

    def copy(self):
        "renvoie une copie de cet etat"
        return Etat( posees = self.posees.copy(), fail = self.fail.copy(),pieces_restantes=self.pieces_restantes.copy())

    def ajoutessai(self,essai):
        "'pose l'essai' i.e ajoute l'essai dans la bonne case de la matrice des essais posés"
        (i,j)=(essai.geti(),essai.getj())
        self.posees[i][j]=essai
        #Remove from essai pieces restantes
        k = 0
        classe=essai.getpiece().getClasse()
        piece=essai.getpiece()
        while self.pieces_restantes[classe][k].getId() != piece.getId():
            k += 1
        self.pieces_restantes[classe].pop(k)


    def retire_essai(self,essai):
        "Retire l'essai des pièces posées et remet la pièce dans les pièces disponibles"
        (i, j) = (essai.geti(), essai.getj())
        self.posees[i][j] = None
        self.ranger_piece(essai.getpiece(), self.getPiecesrestantes())

def egal(e1,e2):
    "Fonction prenant en argument deux essais et renvoyant true s'ils correspondent au même essai, false sinon"
    return( e1.getpiece().getClasse()==e2.getpiece().getClasse() and e1.geti()==e2.geti() and e1.getj()==e2.getj() and e1.getrotation()==e2.getrotation() )

def essai_in(essai,liste):
    "Fonction prenant en argument un essai et une liste d'essais et renvoyant true si l'essai est contenu dans la liste, false sinon"
    appartient=False
    n=len(liste)
    k=0
    while not appartient and k<n:
        if egal(essai,liste[k]):
            appartient=True
        k+=1
    return(appartient)

def creer_Etat(puzzle):
    "Fonction qui crée un état 'vide, initial'"
    size=puzzle.getsize()
    a=np.ndarray(size,dtype=Essai)
    b=np.ndarray(size,dtype=list)
    return (Etat(posees = a, fail = b,pieces_restantes=classe_equivalence(puzzle.getlistpieces())))


def coordnext(essai,size):
    "Fonction qui prend en argument un essai et les dimensions du puzzle"
    "Renvoie les coordonnées du prochain emplacement où une pièce devra être posée en suivant l'ordre de parcours prédéfini"
    (i,j)=(essai.geti(),essai.getj())
    ordreparc=Puzzle.ordreparcours(size)
    for k in range (len(ordreparc)):
        if (i,j)==ordreparc[k]:
            return(ordreparc[k+1])

def essais_voisins(etat,i,j):
    "Fonction qui prend en argument un état et deux coordonnées i,j"
    "Cette fonction renvoie la liste des essais voisins à la position de coordonnée (i,j), triés dans le sens horaire en partant du haut (ie haut, droite, bas, gauche)"
    global E0
    Posees=etat.getPosees()
    (ha,la)=np.shape(Posees)

    listeVoisins=[E0 for _ in range(4)]
    l=[(i-1,j),(i,j+1),(i+1,j),(i,j-1)]
    for k in range(4):
        (i1,j1)=l[k]
        if i1 != -1 and i1!= ha and j1 !=-1 and j1 != la :
                listeVoisins[k]=etat.getEssaipose(i1,j1)
    return listeVoisins

def print_posees(etat):
    "Fonction prenant en argument un état et renvoyant la matrice des identifiants des pièces posées "
    m=etat.getPosees()
    a=np.ndarray(np.shape(m),dtype=int)
    (ha,la)=np.shape(m)
    for i in range(ha):
        for j in range(la):
            if m[i][j]==None:
                a[i][j]=-1
            else:
                p=m[i][j].getpiece()
                a[i][j]=p.getId()
    print(a)

    
    
    


