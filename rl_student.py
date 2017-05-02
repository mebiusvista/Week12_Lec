# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 23:11:12 2015

@author: zhengzhang
"""
import random
import rl_helper

''' a simple case: 0 <-> 1 <-> 2; room #2 is the exit'''
R_simple = [
            [-1, 0, -1],
            [0, -1, 0],
            [-1, 0, 100]
            ]

''' a more complex world, see lecture example '''   
R_room = [
    [-1, -1, -1, -1, 0, -1],
    [-1, -1, -1, 0, -1, 100],
    [-1, -1, -1, 0, -1, -1],
    [-1, 0, 0, -1, 0, -1],
    [0, -1, -1, -1, -1, 100],
    [-1, 0, -1, -1, 0, 100]
    ]
    
class World():
    def __init__(self, rewards, final_state):
        self.rewards = rewards
        self.num_states = len(rewards)
        self.num_acts = len(rewards[0])
        self.final_state = final_state
        
    def is_final_state(self, s):
        return s == self.final_state
        
    def get_num_states(self):
        return self.num_states
    
    def get_num_acts(self):
        return self.num_acts
                
    def get_valid_acts(self, s):
        """TODO"""
        acts = rl_helper.get_valid_acts(self, s)
        return acts
        
    def get_reward_in_state_act(self, s, a):
        return self.rewards[s][a]
        
class Agent():
    def __init__(self, n_state, n_act, gamma = 0.0, epsilon = 0.0):
        self.Q = [ [0 for i in range(n_act)] for j in range(n_state)]
        self.gamma = gamma
        self.epsilon = epsilon
        
    def get_maxQ(self, s):
        return max(self.Q[s])
        
    def get_maxQ_act(self, s, acts):
        max_q = -1
        for a in acts:
            if self.Q[s][a] > max_q:
                max_q = self.Q[s][a]
                max_a = a
            elif self.Q[s][a] == max_q: # make some randomness when tie
                if random.random() < 0.5:
                    max_a = a
        return max_a
        
    def make_move(self, s, valid_moves):   
        """TODO"""
        act = rl_helper.make_move(self, s, valid_moves)
        return act
        
    def update_Q(self, s, a, next_s, r):
        """TODO"""
        rl_helper.update_Q(self, s, a, next_s, r)
        return
        
    def set_Q(self, s, a, val):
        self.Q[s][a] = val
        
    def __str__(self):
        qstr = ''
        for i in range(len(self.Q)):
            qstr += str(self.Q[i]) + '\n'
        return qstr
        
if __name__ == "__main__":
    ''' set up the world'''
    w = World(R_room, 5)
#    w = World(R_simple, 2)
    num_states = w.get_num_states()
    num_actions = w.get_num_acts()
        
    ''' set up the agent '''
    gamma = 0.8
    epsilon = 0.2 
    agent = Agent(num_states, num_actions, gamma, epsilon)
    
    ''' set up the runs '''
    total_iter = 500
    num_iter = 0
    interactive = False
    verbose = False
    report_steps = 100
    
    ''' start learning '''
    while num_iter < total_iter:
        ''' init one random state '''
        s = random.choice(list(range(num_states)))
        moves = [s]
        while True:
            ''' make one move '''
            valid_moves = w.get_valid_acts(s)
            act = agent.make_move(s, valid_moves)
          
#            print(s, act, valid_moves)
            this_reward = w.get_reward_in_state_act(s, act)
            ''' for this example, next state is equal to act '''
            next_s = act
            agent.update_Q(s, act, next_s, this_reward)       
            s = next_s
            
            moves.append(s)
            if w.is_final_state(s):
                break
        
        if verbose:
            print("moves: ", moves)
            
        num_iter += 1
        if num_iter % report_steps == 0:
            print(agent)
            
        if interactive:
            if input('quit [y/n]? ') == 'y':
                break

