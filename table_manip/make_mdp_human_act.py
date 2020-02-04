import itertools

human_readable = False

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

#   we have robot gripper, else, and the other locations for our states
num_place_locs = 5
num_human_locs = 1
num_objects = 3

# TODO need some way to describe which blocks the human will move in a given state
human_displacements = []

human_interupt_prob = 0.1 # Probability of staying in the same state
human_rand_move_prob = 0.1 # Probability of moving into a different legal state


# TODO need some way to describe which blocks are on top of others
# list of which locs must be free to pick/place block at location x
placement_requirements = []
placement_requirements.append([]) # gripper
placement_requirements.append([]) # else
placement_requirements.append([3,4]) # top requires left and right supports
placement_requirements.append([]) # left
placement_requirements.append([]) # right
# print("placement_requirements: ")
# print(placement_requirements)

# list of which locs must be free to pick block at location x
grasp_requirements = []
grasp_requirements.append([]) # gripper
grasp_requirements.append([]) # else
grasp_requirements.append([]) # top
grasp_requirements.append([2]) # left requires top free
grasp_requirements.append([2]) # right requires top free
# print("grasp_requirements: ")
# print(grasp_requirements)

# initial_state_str = "2,1,0"
# initial_state_list = [2,1]
# initial_state_tpl = (2,1,0)

initial_state_str = "1,3,4,0"
initial_state_list = [1,3,4]
initial_state_tpl = (1,3,4,0)

initial_state = State()
initial_state.obj_locs=initial_state_list
initial_state.human_loc=0

def state2i(s):
    r = 0
    power = 1;
    for i in range(num_objects):
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

# Ensure all placement requirement locations are occupied
def isLegalPlacement(index, state):
    loc_list = placement_requirements[index]
    for loc in loc_list:
        loc_occupied = False
        for i in state.obj_locs:
            if i == loc:
                loc_occupied = True
                continue
        if loc_occupied:
            continue
        else:
            return False
    return True

#Ensure no objects obstruct the grasp
def isLegalGrasp(index, state):
    loc_list = grasp_requirements[index]
    for loc in loc_list:
        for i in state.obj_locs:
            if i == loc:
                return False
    return True

def makeStateNeighbors(state):
    neighbors = []
    actions = []

    transitions = []

    #if any object is grasped by the robot:
    grasped_obj = -1
    for i in range(num_objects):
        if state.obj_locs[i] == 0:
            grasped_obj = i
            break
    # The grasped object can be placed at any empty location
    if(grasped_obj != -1):
        # 1 if neighbor is available, -1 otherwise
        available_neighbors = [1]*num_place_locs
        for l in range(num_objects):
            available_neighbors[state.obj_locs[l]] = -1
        for n in range(2,len(available_neighbors)): # Don't count gripper and else region
            if available_neighbors[n] == 1 and isLegalPlacement(n, state):
                s_prime = State()
                s_prime.obj_locs = state.obj_locs.copy()
                s_prime.human_loc = state.human_loc
                s_prime.obj_locs[grasped_obj] = n
                neighbors.append(s_prime)
                T = Transition()
                T.action = "robot places {} at {}".format(grasped_obj, n)
                p_d = (s_prime, 0.9)
                T.prob_distr.append(p_d)
                T.prob_distr.append((state, 0.1))
                transitions.append(T)
        s_prime = State()
        s_prime.obj_locs = state.obj_locs.copy()
        s_prime.human_loc = state.human_loc
        s_prime.obj_locs[grasped_obj] = 1 # We can always use the else region
        neighbors.append(s_prime)
        T = Transition()
        T.action = "robot places {} at ELSE".format(grasped_obj)
        p_d = (s_prime, 0.9)
        T.prob_distr.append(p_d)
        T.prob_distr.append((state, 0.1))
        transitions.append(T)

    # Any object can be grasped
    # TODO: only allow available objects to be grasped (i.e., can't grasp and object with another on top)
    else:
        for i in range(num_objects):
            if isLegalGrasp(i, state):
                s_prime = State()
                s_prime.obj_locs = state.obj_locs.copy()
                s_prime.human_loc = state.human_loc
                s_prime.obj_locs[i] = 0
                neighbors.append(s_prime)
                T = Transition()
                T.action = "robot picks up {}".format(i)
                p_d = (s_prime, 0.9)
                T.prob_distr.append(p_d)
                T.prob_distr.append((state, 0.1))
                transitions.append(T)
            # print(state2str(s_prime))

    # for n in neighbors:
    #     print(state2str(n))
    state.neighbors = neighbors
    state.act_to_reach_neighbor = actions
    state.transitions = transitions

    return neighbors

def createMDPStates():
    s = initial_state

    visited_states = {initial_state_str:initial_state_tpl}
    curr_frontier = []
    all_states = []


    curr_frontier.append(s)

    while(len(curr_frontier) > 0):
        #remove state from frontier and add to visited states
        s = curr_frontier[-1]
        curr_frontier.pop()
        my_tpl = {state2str(s) : state2tpl(s)}
        visited_states.update(my_tpl)
        all_states.append(s)
        #check all neighbors and add new ones to frontier
        neighbors = makeStateNeighbors(s)
        for n in neighbors:
            if state2str(n) in visited_states:
                pass
            else:
                curr_frontier.append(n)
    return all_states

## Print the MDP
print("mdp")
print("")
print("module M1")
print("")
print("    x : [0..{}] init {};".format(num_human_locs*(num_objects**num_place_locs), state2i(initial_state)))

#mylist = getAllObjPlacements(num_objects)

# for i in range(num_human_locs):
#     for s in mylist:
#         print(state2i(i, s))

states = createMDPStates()

for s in states:
    for t in s.transitions:
        if human_readable:
            str = "     "+state2str(s)+ " ->"
            for s_p, pr in t.prob_distr:
                # print(tr)
                # s_p, pr = tr
                str = str + " {}: ".format(pr) + state2str(s_p)+" "
            str = str + ";"
            print(str)
        else:
            str = "    [] x={} ->  ".format(state2i(s))
            for s_p, pr in t.prob_distr:
                # print(tr)
                # s_p, pr = tr
                str = str + " {}:(x'={})+".format(pr, state2i(s_p))
            str = str[:-1] + ";"
            print(str)


print("")
print("endmodule")

print("")
print("// labels")
print("label \"initial\" = (x=0);")


# Certain states aren't possible
# Not sure if these are needed. Probably not necessary if we set the initial state correctly
#     [] x=0 -> (x'=0);
#     [] x=3 -> (x'=3);
#     [] x=5 -> (x'=5);
#     [] x=10 -> (x'=10);
#     [] x=15 -> (x'=15);
#     [] x=16 -> (x'=16);