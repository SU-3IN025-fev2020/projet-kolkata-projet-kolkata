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

    def get_nom(self):
        return "Strat"



class StratAlea(Strat):
    def get_goal(self):
        return random.randint(0,len(Strat.list_r)-1)

    def new_strat(self, i):
        return StratAlea()

    def get_nom(self):
        return "Strat aleatoire"



class StratTetu(Strat) :

    def __init__(self):
        self.goal = random.randint(0,len(Strat.list_r)-1)

    def get_goal(self):
        return self.goal

    def new_strat(self, i):
        return StratTetu()

    def get_nom(self):
        return "Strat tétu"



class StratMoinsRempli(Strat) :

    def get_goal(self):
        if len(Strat.d) == 0 :
            return random.randint(0,len(Strat.list_r)-1)
        return Strat.list_r.index(min(Strat.d, key=Strat.d.get))

    def new_strat(self, i):
        return StratMoinsRempli()

    def get_nom(self):
        return "Strat moins rempli"



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
            if distance != 0 and (distance < dist_mini or dist_mini == -1):
                dist_mini = distance
                rest_plus_proche = i
        return rest_plus_proche

    def new_strat(self, k):
        return StratRestauPlusProche(self.list_posPlayers, k)

    def get_nom(self):
        return "Strat restaurant le plus proche"

class StratRestau :
        list_posPlayers = []
        list_gain = []
        d = dict()

        def __init__(self, list_r, indice_r):
                self.indice_r = indice_r
                self.list_r = listr_r

        def set_list_posPlayers(list_posPlayers):
            Strat.list_posPlayers = list_posPlayers

        def set_list_gain(list_gain):
            Strat.list_gain = list_gain

        def set_gain(self):
            raise NotImplementedError("not implemented set_gain")


        def new_strat(self, i):
            raise NotImplementedError("not implemented new_strat")

        def get_nom(self):
            return "StratRestau"

class StratRestauUnClient (StratRestau) :

    def set_gain(self):
        if len(StratRestau.d.get(self.list_r[self.indice_r])) == 1 :
            list_gain[StratRestau.d.get(self.list_r[self.indice_r])[0]] += 1

    def new_strat(self, i):
        return StratRestauPlusProche(self.list_r, i)

class StratRestauDeuxClientMini (StratRestau) :

    def set_gain(self):
        if len(StratRestau.d.get(self.list_r[self.indice_r])) >= 2 :
            for i in StratRestau.d.get(self.list_r[self.indice_r]) :
                list_gain[i] += 1

    def new_strat(self, i):
        return StratRestauDeuxClientMini(self.list_r, i)

class StratRestauRobinDesBois (StratRestau):

    def set_gain(self):
        max = -1
        max_i = 0
        for i in StratRestau.d.get(self.list_r[self.indice_r]) :
            if list_gain[i] > max :
                max = list_gain[i]
                max_i = i

        list_gain[max_i] = 0
        for i in range(len(list_gain)):
            if i == max_i :
                continue
            list_gain[i] += 1
            max -= 1
            if max == 0:
                break

    def new_strat(self, i):
        return StratRestauRobinDesBois(self.list_r, i)
