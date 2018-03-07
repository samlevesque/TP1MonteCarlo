#cd OneDrive\UDEM\Hiver 2017\Structures de données\Devoirs\TP1

""" VOIR FICHIER PDF INCLU POUR UNE EXPLICATION DU CONCEPT D'ENTIER GENERALISE QUE J'AI DEVELOPPE """



import random
import sys

class GameTree:
    """ Arbre a structure liee grandement epure car on a pas besoin de grand chose """
    class Node:
        __slots__ = '_element', '_parent', '_children'
        def __init__(self, element, children = []):
            self._element = element
            self._children = children

        """ Une optimisation utile est le fait de seulement verifier qui est le gagnant de la partie lorsque
            le scoreboard change, on se sauve du calcul """
        def sample(self, n):
            wins = 0
            parent = self._element
            winner = det_win_game(parent)
            if winner == 0:
                for i in range(n):
                    winner = 0
                    current_game = parent
                    while winner == 0:
                        new_game = random_move(current_game)
                        if(scoreboard_has_changed(new_game, current_game)):
                            winner = det_win_game(new_game)
                            if winner == 1:
                                wins += 1
                        current_game = new_game
            else:
                if win == 1:
                    wins = n
                else:
                    wins = 0
            #print(parent,wins)
            return (parent,wins)
        
        def add_children(self, element):
            child = type(self)(element)
            self._children.append(child)

    def __init__(self, root):
        self._root = self.Node(root)

    """ On construit les niveau de l'arbre, et on a l'option de l'afficher """
    def build_levels(self, n, isPrint):
        
        current_level = [self._root]
        
        for i in range(n):
            if isPrint:
                for n in current_level:
                    entg = n._element
                    ent = degeneralize(entg)
                    print(ent, " ", end="")
                print("")
            next_level = []
            for n in current_level:
                entn = n._element
                for vm in valid_moves(entn):
                    m = move(entn, vm)
                    n.add_children(m)
                for c in n._children:
                    next_level.append(c)
            current_level = next_level
            
    """ Determine et retourne le coup optimal """
    def optimal_move(self, n):
        self.build_levels(1, False)
        """ SPDG, on prend le premier enfant comme optimal de depart """
        optimal = (self._root._children[0]._element, 0)
        for b in self._root._children:
            bwins = b.sample(n)
            if bwins[1] > optimal[1]:
                optimal = bwins
        return optimal[0]

""" Indice de la sous-partie selon la position """
def board_from_i(i):
    return i // 9

""" Indice de la sous-partie opposee selon la position """
def opp_board_from_i(i):
    return i % 9

def val_i(entier, i):
    return entier >> ((80 - i) << 1) & 3

""" Generateur des positions de la sous-partie i """
def cases_board_i(i):
    start = 9*i
    for j in range(9):
        yield start + j

def last(entier):
    return entier >> 162 & 127

""" Lorsqu'on lit un entier pas general, on doit le generaliser et ecrire son scoreboard actuel """
def det_scoreboard(entierg):
    for i in range(9):
        val = det_win_board(entierg, i)
        entierg = write_score(entierg, val, i)
    return entierg

""" Pour eviter de recalculer le gagnant si le dernier coup n'as pas changer le score """
def scoreboard_has_changed(entierg1, entierg2):
    return zai(entierg1 >> 170, 18) != zai(entierg2 >> 170, 18)

def write_score(entierg, val, i):
    bit = bit_from_board(i)
    if val == 0:
        entierg = zai(zai(entierg,bit),bit+1)
    elif val == 1:
        entierg = zai(oai(entierg,bit),bit+1)
    elif val == 2:
        entierg = oai(zai(entierg,bit),bit+1)
    elif val == 3:
        entierg = oai(oai(entierg,bit),bit+1)
    return entierg

""" Determiner le gagnant d'une sous-partie """
def det_win_board(entierg, i):
    cases = list(cases_board_i(i))
    v = []
    for j in range(9):
        v.append(val_i(entierg, cases[j]))
    
    return det_win_from_values(v)

def det_win_from_values(v):
    # 0 1 2
    # 3 4 5
    # 6 7 8
    # on peut simplement regarder lignes,colonnes,diag provenant des cases 0,1,2,3,6
    # 
    
    #ligne 012
    if (v[0] == v[1] == v[2] == 1 or v[0] == v[1] == v[2] == 2):
        #print("board : ", i, " ligne 012 : ", v[0])
        return v[0]
    #colonne 036
    if (v[0] == v[3] == v[6] == 1 or v[0] == v[3] == v[6] == 2):
        #print("board : ", i, " colonne 036 : ", v[0])
        return v[0]
    #diag 048
    if (v[0] == v[4] == v[8] == 1 or v[0] == v[4] == v[8] == 2):
        #print("board : ", i, " diag 048 : ", v[0])
        return v[0]
    #colonne 147
    if (v[1] == v[4] == v[7] == 1 or v[1] == v[4] == v[7] == 2):
        #print("board : ", i, " colonne 147 : ", v[1])
        return v[1]
    #colonne 258
    if (v[2] == v[5] == v[8] == 1 or v[2] == v[5] == v[8] == 2):
        #print("board : ", i, " colonne 258 : ", v[2])
        return v[2]
    #diag 246
    if (v[2] == v[4] == v[6] == 1 or v[2] == v[4] == v[6] == 2):
        #print("board : ", i, " diag 246 : ", v[2])
        return v[2]
    #ligne 345
    if (v[3] == v[4] == v[5] == 1 or v[3] == v[4] == v[5] == 2):
        #print("board : ", i, " ligne 345 : ", v[3])
        return v[3]
    #ligne 678
    if (v[6] == v[7] == v[8] == 1 or v[6] == v[7] == v[8] == 2):
        #print("board : ", i, " ligne 678 : ", v[6])
        return v[6]
    #si pas victoire et une case vide
    if any(value == 0 for value in v):
        #print("board : ", i, " BOARD VALIDE ", 0)
        return 0
    else:
        #print("board : ", i, " BOARD NUL ", 3)
        return 3

""" On recupere la fonction pour determiner le gagnant de la partie """
def det_win_game(entierg):
    if valid_moves(entierg) == None:
        return 3
    cases = list(range(9))
    v = []
    for j in range(9):
        v.append(board_value(entierg, cases[j]))
        
    return det_win_from_values(v)

chars = ['.', 'x', 'o']
mchars = ['.', 'X', 'O']

""" Affichage d'une case """
def print_case(entier, i, li):
    if (i == li):
        return " " + mchars[val_i(entier, i)] + " "
    else:
        return " " + chars[val_i(entier, i)] + " "

def print_grid(entier):
    li = last(entier)
    i = 0
    j = 0
    k = 0
    while i < 81:
        print(print_case(entier, i, li), print_case(entier, i+1, li), print_case(entier, i+2, li), end="")
        print("|", end="")
        i += 9
        j += 1
        if(j == 3):
            print("")
            k +=1
            j = 0
            i -= 24
        if(k == 3):
            print("------------------------------")
            k = 0
            i += 18
            
""" Ecrire un one (1) au bit i """
def oai(entier, i):
    one = 1
    one = one << i
    return one | entier

""" Ecrire un zero (0) au bit i """
def zai(entier, i):
    one = 1
    one = one << i
    return ~one & entier

""" Retourne l'entier generalisee obtenu apres avoir fait le coup en pos.
    Ce coup n'est pas nécessairement valide question flexibilité mais après chaque coup le scoreboard
    est mis a jour """
def move(entierg, pos):
    lastcase = last(entierg)
    dernier_joueur = val_i(entierg, lastcase)
    bitpos = bit_from_pos(pos)
    if(dernier_joueur == 1):
        entierg = oai(zai(entierg, bitpos),bitpos+1)
    else:
        entierg = zai(oai(entierg, bitpos),bitpos+1)
    entierg = save_last_move(entierg, pos)
    #print("AVANT UPDATE")
    entierg = update_scoreboard(entierg, pos)
    #print("APRES UPDATE")
    return entierg

""" Retourne l'indice du bit d'une position sur le board """
def bit_from_pos(pos):
    return -2 *(pos - 80)

""" Retourne le bit ou se trouve le score du board i sur le scoreboard """
def bit_from_board(i):
    return 170 + (18 - 2*(i+1))

""" Retourne l'entier generalisee avec le dernier coup en pos """
def save_last_move(entierg, pos):
    for i in range(7):
        entierg = zai(entierg, i + 162)
    return (pos << 162) + entierg

""" Generalise un entier, c'est a dire lui ajoute le scoreboard """
def generalize(entier):
    temp = (1 << 19) + 1
    for i in range(20):
        entier = zai(entier, i + 169)
    return (temp << 169) + entier

""" Retourne le score du board i """
def board_value(entierg, i):
    return entierg >> 188 - 2*(i+1) & 3

""" Mise a jour du scoreboard selon le dernier move m """
def update_scoreboard(entierg, m):
    board = board_from_i(m)
    val = det_win_board(entierg, board)
    return write_score(entierg, val, board)

""" Generateur des coups possibles a partir d'un entier generalise """
def valid_moves(entierg):
    lm = last(entierg)
    opb = opp_board_from_i(lm)
    if(board_value(entierg, opb) == 0):
        for m in valid_moves_b(entierg, opb):
            yield m
    else:
        for i in range(9):
            if board_value(entierg, i) == 0:
                for m in valid_moves_b(entierg, i):
                    yield m

""" Generateur des coups possibles a partir d'un entier generalise sur le boards b """
def valid_moves_b(entierg, b):
    for i in cases_board_i(b):
        if val_i(entierg, i) == 0:
            yield i

""" Retourne l'entier generalise obtenu en faisant un coup aleatoire parmi les coups valide """
def random_move(entierg):
    movelist = list(valid_moves(entierg))
    if len(movelist) > 0:
        return move(entierg, random.choice(movelist))
    else:
        return entierg

""" Degeneralise un entier pour la sortie """
def degeneralize(entierg):
    entier = entierg
    for i in range(20):
        entier = zai(entier, i + 169)
    return entier

""" MAIN FUNCTIONS """

""" Mode coup optimal """
def noarg(entier):
    entierg = generalize(entier)
    entierg = det_scoreboard(entierg)
    gt = GameTree(entierg)
    optig = gt.optimal_move(1000)
    opti = degeneralize(optig)
    print(opti)
    print(optig)

""" Mode traduction """
def parg(entier):
    print_grid(entier)

""" Mode arbre """
def aarg(profondeur, entier):
    entierg = generalize(entier)
    entierg = det_scoreboard(entierg)
    gt = GameTree(entierg)
    gt.build_levels(profondeur+1, True)

""" Mode random tree """
def rarg(nbcoups, profondeur):
    test = 0
    testg = generalize(test)
    rtest = testg
    for i in range(nbcoups):
        rtest = random_move(rtest)
    entierg = rtest
    gt = GameTree(entierg)
    gt.build_levels(profondeur, True)
    
""" On gere les arguments """
def main(argv):
    """ Si on lance le programme sans arguments """
    if len(sys.argv) < 2:
        print("ERREUR : PAS D'ARGUMENT")
    elif len(sys.argv) > 4:
        print("ERREUR : TROP D'ARGUMENTS")
    else:
        if len(sys.argv) == 2:
            """ Mode coup optimal """
            noarg(int(sys.argv[1]))
        elif len(sys.argv) == 3:
            """ Mode traduction """
            if sys.argv[1] == 'p':
                parg(int(sys.argv[2]))
        elif len(sys.argv) == 4:
            """ Mode arbre """
            if sys.argv[1] == 'a':
                aarg(int(sys.argv[2]), int(sys.argv[3]))
            """ Mode random tree """
            if sys.argv[1] == 'r':
                rarg(int(sys.argv[2]), int(sys.argv[3]))
                
if __name__ == "__main__":
   main(sys.argv[1:])

