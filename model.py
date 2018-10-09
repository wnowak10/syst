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

POSSIBLE_PRIORITIES     = {'prestige':.6, 'cost':.4}
FAMILY_PRIORITY_WEIGHTS = [.3, .3, .3]
MAX_ENDOWMENT_DRAW      = .1  # Most schools draw ~5%. Drawing more than ENDOWMENT_GROWTH_RATE should decrease endowment over time.
NUM_SIMULATIONS         = 1
NUM_TIME_STEPS          = 5
NUM_FAMILIES            = 5
NUM_SCHOOLS             = 3

# ______________________________________________________________________________
# Model

class SchoolModel(Model):
    """A mode to simulate family-school choice.

    A outlined description is as follows:
    1. Initialize `num_schools` # of schools with give parameters.
    2. At each step (a year), we generate `num_families` # of families.
    Each family has a set of priorities and then makes a school choice.
    3. After choosing a school, the school finances and future family 
    decision priorities evolve.
    """
    def __init__(self, num_families, num_schools, family_priority_weights):
        self.num_families              = num_families
        self.num_schools               = num_schools
        # Though we randomly initialize family priorities, this global variable
        # controls macro market preferences. E.g. are families growing more 
        # cost conscious? TO DO: Make this happen as general macro-economy worsens,
        # which should also lower school endowment growth rate. 
        self.family_priority_weights   = family_priority_weights

        # How to take steps -- each agent activeated in random order. 
        self.schedule    = RandomActivation(self)  

        # Create schools
        for i in range(self.num_schools):
            # Parameterize school.
            # TO DO: Implement in a seperate function?
            endowment      = scipy.stats.expon().rvs(1)[0] #random.randint(0,100)
            prestige       = np.abs(np.random.normal(0, 1, 1)[0])
            tuition        = (prestige / 2) # Cost is directly related to prestige.
            annual_fund    = random.randint(0,100)
            efficacy       = np.abs(np.random.normal(0, 1, 1)[0])
            priorities     = helpers.make_random_school_priorities()
            # Endowment draw is 0 if the school only cares about prestige,
            # whereas endownment draw is MAX_ENDOWMENT_DRAW 
            # if school cares only about equity and efficacy. Theory: schools that
            # care about equity and efficacy will spend on current students, whereas 
            # per Gladwell, saving money and building endowment increases reputation
            # at a cost of not adding much immediate value to today's students.
            endowment_draw = MAX_ENDOWMENT_DRAW * (priorities['Equity'] + priorities['Efficacy']) / 1
            # Set a school in city close to 0, remote farther from there. Normal distribution implies
            # more schools closer to 1D center.
            location       = np.random.normal(0, 100, 1)[0]

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

    def step(self, i):
        # schools= [obj for obj in self.schedule._agents.values() if isinstance(obj, agents.SchoolAgent)]
        # prestiges = [i.prestige for i in schools]


        # Each step, create new families.
        # print(i)
        start = self.num_schools  + i * self.num_families
        end   = self.num_schools  + (i + 1) * self.num_families #(self.num_schools  + self.num_families) * (i+1)
        # print(self.num_families)
        # print('start', 'end', start, end)

        for j in range(start, end): # Need to have unique ids.

            # A randomly initialized wealth. As per https://arxiv.org/pdf/cond-mat/0103544,
            # most American's have wealth following exponential distribution.
            # A rough estimation. Here there are no <50 values.
            # TO DO: Think about financial aid.
            wealth   = scipy.stats.expon(50,200).rvs(1)[0]
            
            # What is their top priority? TO DO: Make priorities a weighted average where
            # they care about all priorities but individual families have different weightings.
            priorities = helpers.make_random_family_priorities()
            # print('Family {} has these priorities {}'.format(j, priority))
            # Where they live. Most people live in median place. This is simulating
            # cities versus rural living.
            location = np.random.normal(0, 100, 1)[0] # Set a school in city close to 0, remote farther from there.
            # TO DO, have schools choose or set location based on some more intelligent game theoretic model.

            family   = agents.FamilyAgent(j, self, wealth, priorities, location)
            self.schedule.add(family)
        # start = end + 1
        # end   = end + self.num_families
        self.schedule.step()
        current_families = [obj for obj in self.schedule._agents.values() if isinstance(obj, agents.FamilyAgent)]
        print([i.unique_id for i in current_families])
        for f in current_families:
             self.schedule.remove(f) 

# ______________________________________________________________________________
# Run model.

if __name__=='__main__':
    for _ in range(NUM_SIMULATIONS):
        model = SchoolModel(num_families=NUM_FAMILIES, 
                            num_schools=NUM_SCHOOLS, 
                            family_priority_weights=FAMILY_PRIORITY_WEIGHTS)
        
        helpers.initial_inspection(model)
        
        for i in range(NUM_TIME_STEPS): # How many years to let this run. 
            print('Step {}'.format(i))
            model.step(i)

        helpers.retrospective(model)
    helpers.simulation_retrospective()


























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
# print(empty_model.num_families)