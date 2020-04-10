from tools import gain, fini, strategie
from strat import Strat
from a_start import a_start
import random

import numpy as np

def tournoi(strat, iterations, game):

    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    players = [o for o in game.layers['joueur']]
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    posPlayers = [o.get_rowcol() for o in game.layers['joueur']]

    nbPlayers = len(players)
    list_goal = [None]*nbPlayers
    L = []
    for i in range(len(strat)) :
        for j in range(i+1,len(strat)):
            L.append([strat[i],strat[j]])


    # ==== positionement des joueurs
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates]
    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[j]=(x,y)

    list_Player_strat = [None]*nbPlayers
    classement_f = dict()
    classement_f2 = dict()

    for s in strat:
        classement_f[s.get_nom()] = 0
        classement_f2[s.get_nom()] = 0

    for a in range(len(L)):
        strategie(L[a],list_Player_strat)
    # ==== debut iteration
        liste_final = battle_royal(iterations, posPlayers, list_goal, game, list_Player_strat, False)
        res = 0
        res2 = 0
        for b in range(len(liste_final)):
            if b < (len(liste_final)/2) :
                res += res + liste_final[b]
            else :
                res2 += res2 + liste_final[b]
        if res > res2 :
            classement_f[L[a][0].get_nom()] += 1
        else :
            classement_f[L[a][1].get_nom()] += 1

        classement_f2[L[a][0].get_nom()] += res
        classement_f2[L[a][1].get_nom()] += res2


        print("score strategie", L[a][0].get_nom(),":",res)
        print("score strategie", L[a][1].get_nom(),":",res2)
    print("classement par victoire : ", [(i,classement_f[i]) for i in sorted(classement_f, key=classement_f.get, reverse=True)])
    print("classement par score : ", [(i,classement_f2[i]) for i in sorted(classement_f2, key=classement_f2.get, reverse=True)])


def battle_royal(iterations, posPlayers, list_goal, game, strat, affichage=True):
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    players = [o for o in game.layers['joueur']]


    nbPlayers = len(posPlayers)

    liste_gain = np.zeros(nbPlayers)

    for j in range(iterations):

        # ==== Initialisation des positions d'arriver
        chemin = [None]*nbPlayers
        for k in range(nbPlayers):
            list_goal[k] = goalStates[strat[k].get_goal()]
            chemin[k] = a_start(posPlayers[k], list_goal[k], nbLignes, nbColonnes, wallStates)


        while (not fini(chemin)):
            for i in range(len(chemin)):
                    if len(chemin[i]) == 0:
                        continue
                    next_row,next_col = chemin[i].pop(0)
                    players[i].set_rowcol(next_row,next_col)
                    game.mainiteration()
                    col=next_col
                    row=next_row
                    posPlayers[i] = (row,col)
                    if (row,col) == list_goal[i]:
                        game.mainiteration()
        d = gain(posPlayers, liste_gain, goalStates)
        Strat.repartition(d)

    if affichage:
        for k in range(len(liste_gain)) :
            print("resultat joueur",k)
            print("type de stratégie: ",strat[k].get_nom())
            print("score :", liste_gain[k])
            print("score moyen :", liste_gain[k]/iterations)
    return liste_gain
