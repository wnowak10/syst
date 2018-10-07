"""
a time step is a year

in every year, some number of parent agents decide where to send their child
for school. we assume that they will not move their kid from this school
and the university will get all of their revenue (unless on financial aid)

many abms place models in spatial grid, with the assumption that they walk
randomly and then interact once they hit same spot. we ignore this aspect here,
as often we'll argue that families go on internet to learn about school
choice and thereby are always able to 'interact' with any school they choose

we will incorporate a location / distance parameter, as it is still reasonable
to assume that ppl choose closer school

(university, boarding school?)
"""

# ______________________________________________________________________________
# Imports

import random
import scipy.stats

import matplotlib.pyplot as plt
import numpy as np

from mesa        import Agent, Model
from mesa.time   import RandomActivation
from collections import defaultdict

import agents
import helpers

# ______________________________________________________________________________
# Constants

POSSIBLE_PRIORITIES = {'prestige':.6, 'cost':.4}
NUM_SIMULATIONS = 1
NUM_TIME_STEPS = 1
NUM_FAMILIES = 5
NUM_SCHOOLS = 3

# ______________________________________________________________________________
# Model

class SchoolModel(Model):
    """
    Docstring.
    """
    def __init__(self, num_families, num_schools):
        self.num_agents  = num_families
        self.num_schools = num_schools

        self.schedule    = RandomActivation(self)  # How to take steps -- each agent activeated in random order. 

        # Create schools
        for i in range(self.num_schools):
            endowment      = random.randint(0,100)
            prestige       = random.randint(0,100)
            tuition        = (prestige / 2) # Cost is directly related to prestige.
            annual_fund    = random.randint(0,100)
            efficacy       = random.randint(0,100)
            endowment_draw = random.randint(0,100)

            priorities     = helpers.make_random_school_priorities()
            
            location       = np.random.normal(0, 100, 1)[0] # Set a school in city close to 0, remote farther from there.

            a = agents.SchoolAgent(i, self, 
                            endowment,  
                            prestige, 
                            tuition,
                            annual_fund,
                            efficacy,
                            endowment_draw,
                            priorities,
                            location)
            self.schedule.add(a)

        # Parents
        for j in range(self.num_schools, self.num_agents + self.num_schools): # Need to have unique ids.

            # A randomly initialized wealth. As per https://arxiv.org/pdf/cond-mat/0103544,
            # most American's have wealth following exponential distribution.
            # A rough estimation. Here there are no <50 values.
            # TO DO: Think about financial aid.
            wealth   = scipy.stats.expon(50,200).rvs(1)[0]
            
            # What is their top priority? TO DO: Make priorities a weighted average where
            # they care about all priorities but individual families have different weightings.
            priority = random.choice(list(POSSIBLE_PRIORITIES.keys()))
            # Where they live. Most people live in median place. This is simulating
            # cities versus rural living.
            location = np.random.normal(0, 100, 1)[0] # Set a school in city close to 0, remote farther from there.
            # TO DO, have schools choose or set location based on some more intelligent game theoretic model.

            parent   = agents.FamilyAgent(j, self, wealth, priority, location)
            self.schedule.add(parent)

    def step(self):
        schools= [obj for obj in self.schedule._agents.values() if isinstance(obj, agents.SchoolAgent)]
        prestiges = [i.prestige for i in schools]
        self.schedule.step()

# ______________________________________________________________________________
# Run model.

if __name__=='__main__':
    model = SchoolModel(num_families = NUM_FAMILIES, num_schools = NUM_SCHOOLS)

    for _ in range(NUM_SIMULATIONS):
        model = SchoolModel(num_families=NUM_FAMILIES, num_schools=NUM_SCHOOLS)
        helpers.initial_inspection(model)
        for i in range(NUM_TIME_STEPS): # How many years to let this run. 
            # print('Step {}'.format(i))
            model.step()

    helpers.retrospective(model)


























# print(model.schedule.agents_by_breed)
# print('\n')
# print(model.schedule._agents)
# print(model.schedule._agents.values())
# print([x for x in model.schedule._agents.values() if isinstance(x, type(FamilyAgent())))
# print([obj.wealth for obj in model.schedule._agents.values() if isinstance(obj, FamilyAgent)])

# print(model.schedule.agents[0].prestige, model.schedule.agents[1].prestige)
# agent_wealth = [a.x for a in model.schedule.agents]
# print(agent_wealth)
# plt.hist(agent_wealth)
# plt.show()


# # nx.draw(DG, with_labels=True, font_weight='bold')
# # plt.show()


# import networkx as nx
# # G = G = nx.Graph() #nx.petersen_graph()
# DG = nx.DiGraph()
# print(DG.number_of_nodes())
# print(DG.number_of_edges())
# empty_model = MoneyModel(10)
# empty_model.step()
# print(empty_model.num_agents)