
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

def initial_inspection(model):
    schools= [obj for obj in model.schedule._agents.values() if isinstance(obj, SchoolAgent)]
    families= [obj for obj in model.schedule._agents.values() if isinstance(obj, FamilyAgent)]

    print('priority', [x.priority for x in families])
    print('family wealth' ,[x.wealth for x in families])
    print('prestige', [y.prestige for y in schools])
    print('endowments', [y.endowment for y in schools])
    print('\n')

def retrospective(model):
    schools= [obj for obj in model.schedule._agents.values() if isinstance(obj, SchoolAgent)]
    families= [obj for obj in model.schedule._agents.values() if isinstance(obj, FamilyAgent)]

    print('priority', [x.priority for x in families])
    print('family wealth' ,[x.wealth for x in families])
    print('prestige', [y.prestige for y in schools])
    print('endowments', [y.endowment for y in schools])
