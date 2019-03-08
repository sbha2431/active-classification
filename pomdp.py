from mdp import MDP
from nfa import NFA
import numpy as np


class POMDP(MDP):
    def __init__(self, MDP,gwg):
        # we call the underlying NFA constructor but drop the probabilities
        # trans = [(s, a, t) for s, a, t, p in transitions]
        # super(super(MDP, self).__init__(states, alphabet, trans),self)
        # # in addition to the NFA we need a probabilistic transition
        # # function
        # self._prob_cache = dict()
        # for s, a, t, p in transitions:
        #     self._prob_cache[(s, a, t)] = p
        # self._prepare_post_cache()
        self.MDP = MDP
        self.Observations = []
        for i in range(2): #Number of agents -- hardcoded
            obs = dict()
            for s in self.MDP.states:
                obs.update({s:self.observation_model(s,gwg,i)})
            self.Observations.append(obs)

    def observation_model(self,s,gwg,i):
        # 8-bit observation
        z_vec = np.zeros(shape=(8,),dtype=int)
        one_index = []
        if s[i] in gwg.left_edge:
            one_index += [0,1,2]
        if s[i] in gwg.right_edge:
            one_index += [4,5,6]
        if s[i] in gwg.top_edge:
            one_index += [2,3,4]
        if s[i] in gwg.bottom_edge:
            one_index += [0,6,7]
        co_ords = []
        for j in range(2):
            co_ords.append(gwg.coords(s[j]))
        active_state = co_ords[i]
        del co_ords[i]
        obs_state = co_ords[0]
        diff_state = tuple(np.subtract(active_state,obs_state))
        loc_dict = {(-1,1):0,(0,1):1,(1,1):2,(1,0):3,(1,-1):4,(0,-1):5,(-1,1):6,(-1,0):7}
        if diff_state in loc_dict:
                one_index += [loc_dict[diff_state]]
        z_vec[list(set(one_index))] = 1
        return self.obs_vec2int(z_vec)

    def obs_vec2int(self,z_vec):
        z_bin = ''.join(map(str,z_vec))
        z_int = int(z_bin,2)
        return z_int

    def write_to_file(self,filename,initial,agent_no=0,targets=set()):
        file = open(filename, 'w')
        self.MDP._prepare_post_cache()
        file.write('|S| = {}\n'.format(len(self.MDP.states)))
        file.write('|A| = {}\n'.format(len(self.MDP.alphabet)))
        file.write('s0 = {}\n'.format(list(self.MDP.states).index(initial)))
        if len(targets)>0:
            stri = 'targets = ('
            for t in targets:
                stri += '{} '.format(t)
            stri = stri[:-1]
            stri+=')\n'
            file.write(stri)

        file.write("s o a s' o' p\n")
        for s in self.MDP.states:
            for a in self.MDP.available(s):
                for t in self.MDP.post(s,a):
                    file.write('{} {} {} {} {} {}\n'.format(list(self.MDP.states).index(s),self.Observations[agent_no][s],a,list(self.MDP.states).index(t),self.Observations[agent_no][t],self.MDP.prob_delta(s,a,t)))