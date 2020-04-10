from tools import gain, fini, strategie
from strat import Strat
from a_start import a_start

import numpy as np

def tournoi(Lstrat, Lplayer, nb_tour, game):
    return None

    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize

    nbPlayers = len(Lplayer)
    list_goal = [None]*nbPlayers
    L = []
    for i in range(len(strat)) :
        for j in range(len(strat[i+1:])):
            L.append([strat[i],strat[j]])


    # ==== positionement des joueurs
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates]
    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[j]=(x,y)

    # ==== debut iteration
    battle_royal(iterations, goalStates, posPlayers,
                list_goal, wallStates, game, strat, players)



def battle_royal(iterations, goalStates, posPlayers, list_goal, wallStates,
                game, strat, players):
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
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

    for k in range(len(liste_gain)) :
        print("resultat joueur",k)
        print("type de stratégie: ",strat[k].get_nom())
        print("score :", liste_gain[k])
        print("score moyen :", liste_gain[k]/iterations)
