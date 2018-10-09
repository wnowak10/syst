
import numpy as np

from agents import *

def make_random_school_priorities():
    priority_list     = ['Equity', 'Prestige', 'Efficacy']

    # Generate random probability distribution.
    priority_dist = np.random.random_integers(0,100,len(priority_list))
    probs = priority_dist / sum(priority_dist)
    
    priorities = {}
    for (item, prob) in zip(priority_list, probs):
        priorities[item] = prob
    return priorities

def make_random_family_priorities(self):
    # print('in the make fam priorities')
    # print(self.family_priority_weights)
    priority_list     = ['Prestige', 'Efficacy', 'Cost']

    # Generate random probability distribution.
    priority_dist = np.random.random_integers(0,100,len(priority_list))
    probs = priority_dist / sum(priority_dist)
    
    priorities = {}
    for (item, prob) in zip(priority_list, probs):
        priorities[item] = prob
    return priorities

def initial_inspection(model):
    schools= [obj for obj in model.schedule._agents.values() if isinstance(obj, SchoolAgent)]
    families= [obj for obj in model.schedule._agents.values() if isinstance(obj, FamilyAgent)]

    # print('priority', [x.priority for x in families])
    # print('family wealth' ,[x.wealth for x in families])
    # print('prestige', [y.prestige for y in schools])
    print('Initial endowments', [y.endowment for y in schools])
    # print('\n')

def retrospective(model):
    schools= [obj for obj in model.schedule._agents.values() if isinstance(obj, SchoolAgent)]
    families= [obj for obj in model.schedule._agents.values() if isinstance(obj, FamilyAgent)]

    # print('priority', [x.priority for x in families])
    # print('family wealth' ,[x.wealth for x in families])
    # print('prestige', [y.prestige for y in schools])
    print('Ending endowments', [y.endowment for y in schools])

def simulation_retrospective():
    """A function to see general patters from N runs of a k time step process.
    """
    return
