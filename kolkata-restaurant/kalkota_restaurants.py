# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random
import numpy as np
import sys




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 144  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

def main():

    #for arg in sys.argv:
    iterations = 20 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()





    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)


    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)


    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)


    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)

    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates]

    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------

    posPlayers = initStates


    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[j]=(x,y)





    #-------------------------------
    # chaque joueur choisit un restaurant
    #-------------------------------

    restau=[0]*nbPlayers
    for j in range(nbPlayers):
        c = random.randint(0,nbRestaus-1)
        print(c)
        restau[j]=c


    #-------------------------------
    # a* tetu
    #-------------------------------
    from a_start import a_start
    from strat import Strat
    from strat import StratAlea
    from strat import StratTetu
    from strat import StratMoinsRempli
    from strat import StratRestauPlusProche



    # Strat.set_nb_j(nbPlayers)
    Strat.set_list_r(goalStates)

    def gain(posPlayers, liste_gain, pos_res):
        d = dict()
        for i in pos_res :
            d[i] = []
        for i in range(len(posPlayers)):
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



    def strategie(L, strat):
        for j in range(len(L)):
            for i in range(j*nbPlayers//len(L), min((j+1)*nbPlayers//len(L), len(strat))):
                strat[i] = L[j].new_strat(i)




    liste_gain = np.zeros(nbPlayers)

    strat = [None]*nbPlayers
    # L = [StratTetu(), StratAlea(), StratMoinsRempli(), StratRestauPlusProche(posPlayers,0)]

    L = [StratRestauPlusProche(posPlayers,0)]


    strategie(L, strat)

    list_goal = [None]*nbPlayers

# ==== debut iteration
    for j in range(iterations):
        chemin = [None]*nbPlayers
        #print(chemin,"\n")
        #print(nbPlayers,"\n")


        for k in range(nbPlayers):
            list_goal[k] = goalStates[strat[k].get_goal()]
            chemin[k] = a_start(posPlayers[k], list_goal[k], 20, 20, wallStates)


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
                        print ("Le joueur ", i, " est à son restaurant.")
        d = gain(posPlayers, liste_gain, goalStates)
        Strat.repartition(d)


    print("resultat :", liste_gain)

    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------





"""
    # bon ici on fait juste plusieurs random walker pour exemple...

    for i in range(iterations):

        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            row,col = posPlayers[j]

            x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            next_row = row+x_inc
            next_col = col+y_inc
            # and ((next_row,next_col) not in posPlayers)
            if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                players[j].set_rowcol(next_row,next_col)
                print ("pos :", j, next_row,next_col)
                game.mainiteration()

                col=next_col
                row=next_row
                posPlayers[j]=(row,col)




            # si on est à l'emplacement d'un restaurant, on s'arrête
            if (row,col) == restau[j]:
                #o = players[j].ramasse(game.layers)
                game.mainiteration()
                print ("Le joueur ", j, " est à son restaurant.")
               # goalStates.remove((row,col)) # on enlève ce goalState de la liste


                break
"""

pygame.quit()





if __name__ == '__main__':
    main()
