from config_file import *


class Transition:
    action=""
    prob_distr = [] # list of <new state, probability>

    def __init__(self):
        self.action=""
        self.prob_distr=[]

class State:
    obj_locs=[]
    human_loc=0
    neighbors = []
    act_to_reach_neighbor = []
    transitions = [] # list of transitions

    def __init__(self):
        self.obj_locs=[]
        self.human_loc=0
        self.neighbors=[]

def state2i(s):
    r = 0
    power = 1;
    for i in range(len(s.obj_locs)):
        r = r + s.obj_locs[i] * power
        power = power*num_place_locs
    r = r + s.human_loc * power
    return r

def state2tpl(s):
    tpl = ( )
    for i in s.obj_locs:
        tpl = tpl + (i,)
    tpl = tpl + (s.human_loc,)
    return tpl

def state2str(s):
    str = "("
    for i in s.obj_locs:
        str = str + "{},".format(i)
    str = str + "{}".format(s.human_loc)
    return str+")"