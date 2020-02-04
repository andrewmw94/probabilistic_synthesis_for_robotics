from mdp import *
from config_file import *
import build_mdp



initial_state = State()
initial_state.obj_locs=initial_state_list
initial_state.human_loc=0

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

states = build_mdp.createMDPStates(initial_state, initial_state_str, initial_state_tpl)

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