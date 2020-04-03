import random
import math

class Strat:
    list_r = []
    d = dict()


    def set_list_r(list_r):
        Strat.list_r = list_r

    def get_goal(self):
        raise NotImplementedError("not implemented get_goal")

    def repartition(d):
        for key, value in d.items():
            d[key] = len(value)
        Strat.d = d

    def new_strat(self, i):
        raise NotImplementedError("not implemented new_strat")




class StratAlea(Strat):
    def get_goal(self):
        return random.randint(0,len(Strat.list_r)-1)

    def new_strat(self, i):
        return StratAlea()





class StratTetu(Strat) :

    def __init__(self):
        self.goal = random.randint(0,len(Strat.list_r)-1)

    def get_goal(self):
        return self.goal

    def new_strat(self, i):
        return StratTetu()



class StratMoinsRempli(Strat) :

    def get_goal(self):
        if len(Strat.d) == 0 :
            return random.randint(0,len(Strat.list_r)-1)
        return Strat.list_r.index(min(Strat.d, key=Strat.d.get))

    def new_strat(self, i):
        return StratMoinsRempli()



class StratRestauPlusProche(Strat) :

    def __init__(self, list_posPlayers, indice_postPlayers):
        self.list_posPlayers = list_posPlayers
        self.indice_postPlayers = indice_postPlayers

    def get_goal(self):
        dist_mini = -1
        rest_plus_proche = 0
        px, py = self.list_posPlayers[self.indice_postPlayers]
        for i in range(len(Strat.list_r)) :
            rx, ry = Strat.list_r[i]
            distance = abs(px - rx) + abs(py - ry)
            if (distance != 0 and (distance < dist_mini) or dist_mini == -1):
                dist_mini = distance
                rest_plus_proche = i
        return rest_plus_proche

    def new_strat(self, k):
        return StratRestauPlusProche(self.list_posPlayers, k)
