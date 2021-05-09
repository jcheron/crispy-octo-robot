import time
from EssaiEtat import *

nb_try = 0


def nonFini(puzzle, etat):
    " Prend en argument le puzzle et l'état courant et renvoie True si le puzzle a été résolu complètement, False sinon"

    (ha, la) = puzzle.getsize()
    (i, j) = Puzzle.ordreparcours((ha, la))[-1]
    return (etat.getEssaipose(i, j) == None)


def match(essai, listeVoisins):
    "Fonction qui prend en argument un essai et la liste de ses Voisins"
    "Cette fonction renvoie True si l'essai est compatible avec les essais préalablement posés autour, et False sinon"
    p0, r0 = essai.getpiece(), essai.getrotation()
    test = [0, 0, 0, 0]
    for k in range(len(listeVoisins)):
        if listeVoisins[k] == None:
            test[k] = 1
        else:
            pk, rk = listeVoisins[k].getpiece(), listeVoisins[k].getrotation()
            if (pk.rotate(rk)[(k + 2) % 4] + p0.rotate(r0)[k]) == 0:
                test[k] = 1
    return (test == [1, 1, 1, 1])


def match_couleur(essai, listeVoisins, c):
    if c == None:
        return True
    if c == 1:
        p0 = essai.getpiece()
        test = True
        for e in listeVoisins:
            if e != None and e.getpiece().getId() != -1 and p0.getCouleur() + e.getpiece().getCouleur() != 1:
                test = False
        return test


def validation(essai, etat, listeVoisins, c):
    "Fonction qui prend en argument un essai, un état et la liste de voisins de la pièce de l'essai"
    "Elle teste si un essai peut être inséré avec succès et renvoie True si c'est le cas, False sinon"
    #if not essai_in(essai, etat.getlistfail(essai.geti(), essai.getj())):
    return match(essai, listeVoisins) and match_couleur(essai, listeVoisins, c)


def get_valid_pieces(etat, puzzle,lastEssai):
    "Fonction prenant en argument un état et un puzzle et renvoyant un essai choisi pour aller à la place suivante de façon à ce que l'essai soit validé et n'ait pas déjà été testé"
    "Renvoie -1 si aucun essai ne peut plus être posé"
    c = puzzle.getC()
    pieces_restantes = etat.pieces_restantes
    if lastEssai == None:
        (i, j) = (0, 0)
    else:
        (i, j) = coordnext(lastEssai, puzzle.getsize())
    listeVoisins = essais_voisins(etat, i, j)
    result = []
    for k in range(len(pieces_restantes)):
        for r in range(4):
            if pieces_restantes[k] != []:
                essai = Essai(piece=pieces_restantes[k][0], i=i, j=j, rotation=r)
                if validation(essai, etat, listeVoisins, c):
                    result.append(essai)
    return result


def check_piece(puzzle, status, counter,lastEssai):
    global nb_try
    if not nonFini(puzzle, status):
        print_posees(status)
        print("Résolution en %d étapes" % counter)
        return True
    else:
        essais = get_valid_pieces(status, puzzle, lastEssai)
        for essai in essais:
            # add piece in status
            status.ajoutessai(essai)
            lastEssai = essai
            if check_piece(puzzle, status, counter + 1,lastEssai):
                return True
            # remove piece from status //Back-tracking
            status.retire_essai(essai)
            nb_try += 1
    return False


def resolution(puzzle):
    "Prend en argument le puzzle et renvoie l'état final du puzzle"
    tic = time.perf_counter()
    courant = creer_Etat(puzzle)

    if not check_piece(puzzle, courant, 0, None):
        print('Résolution impossible!')
    toc = time.perf_counter()
    print('\a', "\n timer=", toc - tic, "secondes \n compteur des ratés=", nb_try, "\n ******************* tadam *********************")
