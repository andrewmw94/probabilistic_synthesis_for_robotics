num_place_locs = 5
num_human_locs = 1
num_objects = 3

def state2i(s):
    r = 0
    power = 1;
    for i in range(len(s)):
        r = r + s[i] * power
        power = power*num_place_locs
    return r

#the goal states
states = [[2,3,4],
          [2,4,3],
          [3,2,4],
          [3,4,2],
          [4,2,3],
          [4,3,2]]


for state in states:
    print(state)
    print(state2i(state))
    print("=============")