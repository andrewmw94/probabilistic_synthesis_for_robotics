from mdp import *
from config_file import *

# Ensure all placement requirement locations are occupied
def isLegalPlacement(loc_index, state):
    loc_list = placement_requirements[loc_index]
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
def isLegalGrasp(loc_index, state):
    loc_list = grasp_requirements[loc_index]
    for loc in loc_list:
        for i in state.obj_locs:
            if i == loc:
                return False
    return True

def genHumanDisturbances(state):
    array = []
    graspable_objs = []
    for obj_i in range(len(state.obj_locs)):
        if isLegalGrasp(state.obj_locs[obj_i], state):
            graspable_objs.append(obj_i)
    legal_places = []
    for loc in range(num_place_locs):
        if isLegalPlacement(loc, state):
            legal_places.append(loc)
    # TODO: For now we assume equal probability of each transfer
    prob = human_interupt_prob*human_rand_move_prob/(len(graspable_objs)*len(legal_places))
    for obj_i in graspable_objs:
        for loc in legal_places:
            s_prime = State()
            s_prime.obj_locs = state.obj_locs.copy()
            s_prime.human_loc = state.human_loc
            s_prime.obj_locs[obj_i] = loc
            array.append((s_prime, prob))
    return array

def makeStateNeighborsRobotPlaceObjAtI(state, grasped_obj, loc):
    array = []
    s_prime = State()
    s_prime.obj_locs = state.obj_locs.copy()
    s_prime.human_loc = state.human_loc
    s_prime.obj_locs[grasped_obj] = loc
    T = Transition()
    T.action = "robot places {} at {}".format(grasped_obj, loc)
    p_d = (s_prime, 1-human_interupt_prob)
    T.prob_distr.append(p_d)
    T.prob_distr.append((state, human_interupt_prob*(1-human_rand_move_prob)))

    # Human does interupt and does move.
    # Move to state with different transfer
    for pd in genHumanDisturbances(state):
        T.prob_distr.append(pd)

    array.append((s_prime, T))
    return array

def makeStateNeighborsRobotPlaceObjAtElse(state, grasped_obj):
    array = []
    s_prime = State()
    s_prime.obj_locs = state.obj_locs.copy()
    s_prime.human_loc = state.human_loc
    s_prime.obj_locs[grasped_obj] = 1 # We can always use the else region
    T = Transition()
    T.action = "robot places {} at ELSE".format(grasped_obj)
    p_d = (s_prime, 1-human_interupt_prob)
    T.prob_distr.append(p_d)

    T.prob_distr.append((state, human_interupt_prob*(1-human_rand_move_prob)))

    # Human does interupt and does move.
    # Move to state with different transfer
    for pd in genHumanDisturbances(state):
        T.prob_distr.append(pd)

    array.append((s_prime, T))
    return array

# cases:
# Human interupts robot
#   And Human moves object
#   And Human doesn't move object
# Human doesn't interup robot
#   And Human moves object
#   And Human doesn't move object
def makeStateNeighborsRobotGraspObjI(state, obj_index):
    array = []
    s_prime = State()
    s_prime.obj_locs = state.obj_locs.copy()
    s_prime.human_loc = state.human_loc
    s_prime.obj_locs[obj_index] = 0
    T = Transition()
    T.action = "robot picks up {}".format(obj_index)
    # Human doesn't interupt and doesn't move
    # Go to intended state
    p_d = (s_prime, 1-human_interupt_prob)
    T.prob_distr.append(p_d)

    # Human does interupt and doesn't move
    # Stay in original state
    T.prob_distr.append((state, human_interupt_prob*(1-human_rand_move_prob)))

    # Human doesn't interupt and does move
    # Ignore for now because it's hard to calculate what doesn't interupt

    # Human does interupt and does move.
    # Move to state with different transfer
    for pd in genHumanDisturbances(state):
        T.prob_distr.append(pd)


    array.append((s_prime, T))
    return array

def makeStateNeighbors(state):
    neighbors = []
    transitions = []

    #if any object is grasped by the robot:
    grasped_obj = -1
    for i in range(num_objects):
        if state.obj_locs[i] == 0:
            grasped_obj = i
            break
    # The grasped object can be placed at legal empty location
    if(grasped_obj != -1):
        # 1 if neighbor is available, -1 otherwise
        available_neighbors = [1]*num_place_locs
        for l in range(num_objects):
            available_neighbors[state.obj_locs[l]] = -1
        for n in range(2,len(available_neighbors)): # Don't count gripper and else region
            if available_neighbors[n] == 1 and isLegalPlacement(n, state):
                neighbs = makeStateNeighborsRobotPlaceObjAtI(state, grasped_obj, n)
                for s_prime, transition in neighbs:
                    neighbors.append(s_prime)
                    transitions.append(transition)
        # We can fit any object into the ELSE region
        neighbs = makeStateNeighborsRobotPlaceObjAtElse(state, grasped_obj)
        for s_prime, transition in neighbs:
            neighbors.append(s_prime)
            transitions.append(transition)

    # Try grasping any object
    else:
        for i in range(num_objects):
            if isLegalGrasp(i, state):
                neighbs = makeStateNeighborsRobotGraspObjI(state, i)
                for s_prime, transition in neighbs:
                    neighbors.append(s_prime)
                    transitions.append(transition)

    state.neighbors = neighbors
    state.transitions = transitions

    return neighbors

def createMDPStates(initial_state, initial_state_str, initial_state_tpl):
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