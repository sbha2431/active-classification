from gridworld import *
from mdp import MDP
import visibility

# Instantiate gridworld
nrows = 7
ncols = 7
initial = [42]
moveobstacles = [7,28,5]
targets = [[]]
obstacles = [16,17,18,25,39,38,37]
regionkeys = {'pavement','gravel','grass','sand','deterministic'}
regions = dict.fromkeys(regionkeys,{-1})
regions['deterministic']= range(nrows*ncols)
gwg = Gridworld(filename=None,initial=initial, nrows=nrows, ncols=ncols, nagents=1, targets=targets, obstacles=obstacles, moveobstacles=moveobstacles,regions=regions)
gwg.render()
gwg.draw_state_labels()
gwg.save('Examples/NN_verification_7x7.png')

# Create MDP from gridworld
states = range(gwg.nstates)
alphabet = [0,1,2,3] # North, south, west, east
transitions = []
for s in states:
    for a in alphabet:
        for t in np.nonzero(gwg.prob[gwg.actlist[a]][s])[0]:
            p = gwg.prob[gwg.actlist[a]][s][t]
            transitions.append((s, alphabet.index(a), t, p))

mdp = MDP(states, set(alphabet),transitions)

# Construct visibility function
visdist = 4
invisibilityset = dict.fromkeys(gwg.states)
for s in gwg.states:
    invisibilityset[s] = visibility.invis(gwg,s,visdist)
    if s in gwg.obstacles:
        invisibilityset[s] = {-1}

# Create Markov chains for moving obstacles
### Insert code here
# MC = mdp.construct_MC(policy_for_movingobstacle)

# Construct product mdp
#productmdp = mdp.constructProductfromMC(MC)

