import random


class Strat:
    list_goal_tetu = []
    list_r = []
    nb_j = 0

    def set_nb_j(nb_j):
        Strat.nb_j = nb_j

    def set_list_r(list_r):
        Strat.list_r = list_r

    def initTetu():
        Strat.list_goal_tetu = [None]*Strat.nb_j
        for i in range(Strat.nb_j):
            Strat.list_goal_tetu[i] = Strat.stratRand()


    def stratRand():
        return random.randint(0,len(Strat.list_r)-1)

    def stratTetu(id_p):
        if len(Strat.list_goal_tetu) == 0:
            Strat.initTetu()
        return Strat.list_goal_tetu[id_p]
