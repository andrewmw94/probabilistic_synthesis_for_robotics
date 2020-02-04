human_readable = False


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