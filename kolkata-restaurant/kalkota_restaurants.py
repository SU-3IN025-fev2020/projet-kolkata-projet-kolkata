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
import matplotlib.pyplot as plt




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
    game.fps = 250  # frames per second
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

    from tools import gain, fini, strategie

    from tournoi import battle_royal, tournoi


    # Strat.set_nb_j(nbPlayers)
    Strat.set_list_r(goalStates)


    strat = [None]*nbPlayers
    L=[]
    L.append(StratTetu())
    L.append(StratAlea())
    L.append(StratMoinsRempli())
    L.append(StratRestauPlusProche(posPlayers,0))


    strategie(L, strat)

    list_goal = [None]*nbPlayers

# ==== debut iteration
    # battle_royal(iterations, posPlayers, list_goal, game, strat)

    nb_essai = 200
    nb_tour = 20
    res = dict()
    names = []
    classement = []
    scores = []
    for i in L :
        res[i.get_nom()] = [0,0]
    for i in range(nb_essai):
        res1, res2 = tournoi(L, nb_tour, game)
        for j in range(len(res1)):
            res[res1[j][0]][0] = res[res1[j][0]][0] + res1[j][1]/nb_essai
            res[res2[j][0]][1] = res[res2[j][0]][1] + res2[j][1]/nb_essai

    for key, value in res.items():
        names.append(key)
        classement.append(value[0])
        scores.append(value[1])

    plt.figure(figsize=(20, 20))
    plt.gcf().subplots_adjust(left = 0.19, bottom = 0.23, right = 1.0, top = 0.94, wspace = 0.20, hspace = 0)
    plt.subplot(131)
    plt.bar(names, classement)
    plt.xticks(rotation = 'vertical')
    plt.subplot(132)
    plt.bar(names, scores)
    plt.xticks(rotation = 'vertical')
    plt.suptitle('Résultat du classement et des scores du tournoi')
    plt.show()

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
