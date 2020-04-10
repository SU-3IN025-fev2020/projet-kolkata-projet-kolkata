import random


def gain(posPlayers, liste_gain, pos_res):
    d = dict()
    for i in pos_res :
        d[i] = []
    for i in range(len(posPlayers)):
        if posPlayers[i] in d:
            d[posPlayers[i]].append(i)
    for key, value in d.items():
        if len(value) == 1 :
            liste_gain[value[0]] = liste_gain[value[0]] + 1
        elif len(value) > 1 :
            i = random.randint(0, len(value)-1)
            liste_gain[value[i]] = liste_gain[value[i]] + 1
    return d

def fini(chemin):
    for i in chemin:
        if len(i) > 0:
            return False
    return True


def strategie(L, strat_player):
    for j in range(len(L)):
        for i in range(j*len(strat_player)//len(L), min((j+1)*len(strat_player)//len(L), len(strat_player))):
            strat_player[i] = L[j].new_strat(i)
