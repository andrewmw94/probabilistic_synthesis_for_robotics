# Description:

Code to generate an MDP for the manipulation domain from previous works (e.g., He et al. ICRA2019). This is meant to be used with PRISM to synthesize optimal policies.


# To run the code:

- Build the domain file with:
`Python3 print_mdp.py > domain.nm`
- Modify the mdp to include the goal states (you can use compute_state_int.py) to calculate the correct integers for each state
- Write the LTL spec you want (see ltl.props)
- Run Prism with options to save the optimal policy:
`prism domain.nm ltl.props --exportadv prism_adv --exportstates prism_adv_states`
