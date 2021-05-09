"----------------------------------------------------------------------------------------------------------------------"
class Piece:
    "Une pièce est définie par:"
    "- id: un identifiant (entier compris entre 0 et le nombre de pièces du puzzle, représentant le numéro de la pièce (numérotées de gauche vers la droite en commençant par la haut"
    "- bord : une liste représentant les quatre bords de la pièce (dans l'ordre haut, droite, bas, gauche)"
    "- rotation : un entier compris entre 0 et 3 représentant la rotation de la pièce"
    "- classe :"

    def __init__(self,id,bord,rotation=None,classe=None,couleur=None):
        self.id=id
        self.bord=bord
        self.rotation=rotation
        self.classe=classe
        self.couleur=couleur

    def getId(self):
        return(self.id)

    def getBord(self):
        return(self.bord)

    def getRotation(self):
        return(self.rotation)
    
    def getClasse(self) :
        return(self.classe)
    
    def getCouleur(self) :
        return(self.couleur)

    def rotate(self,tour):
        "renvoie une liste correspondant au bord de la pièce tourné de x tours dans le sens horaire"
        L=(self.bord)
        M=[]
        for i in range (len(L)):
            M.append(L[((i-tour+len(L))%(len(L)))])
        return(M)
    
    def set_classe(self,classe) :
        self.classe=classe
    
    def set_couleur(self,couleur) :
        self.couleur=couleur

def print_listepieces(liste) :
    "Fonction prenant en argument une liste de pièces et renvoyant la liste de leurs identifiants"
    L=[]
    for k in liste :
        L.append(k.getId())
    return(L)

def print_listedelistesdepieces(listedeliste):
    L=[]
    for l in listedeliste:
        L.append(print_listepieces(l))
    return L
            
def compare_pieces(p1,p2):
    "Fonction prenant en argument deux pièces et renvoyant True si elles sont égales, False sinon"
    l2=p2.getBord()
    k=0
    if p1.getCouleur()==p2.getCouleur():
            while k<4:
                if p1.rotate(k)==l2:
                    return True
                k+=1
    return False

def piece_in(p,liste):
    "Fonction renvoyant l'indice de la pièce p dans liste, renvoie -1 si p n'appartient pas à liste"
    n=len(liste)
    i=0
    while i<n and not (compare_pieces(p, liste[i])):
        i+=1
    if i<n:
        return i
    return -1

def classe_equivalence(liste):
    "Fonction créant une liste de listes des différentes pièces de 'liste' appartenant à la même classe d'équivalence"
    L=[[liste[0]]]
    liste[0].set_classe(0)
    classe=[0]+[-1]*(len(liste)-1)
    for k in range(1,len(liste)):
        p=liste[k]
        i=piece_in(p,liste[:k])
        if i==-1:
            classe[k]=len(L)
            L.append([p])
            p.set_classe(classe[k])
        else:
            p.set_classe(classe[i])
            L[classe[i]].append(p)
    return(L)
            





        



