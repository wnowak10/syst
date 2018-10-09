# Imports 
# ______________________________________________________________________________

import numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation

# Constants 
# ______________________________________________________________________________

SCANDAL_PROBABILITY   = .03 # Use Choate as representative -- ~3/125 ~~ 3%
ENDOWMENT_GROWTH_RATE = .07 # Standard S&P returns. Assume efficient market hypothesis. 
WEIGHT_DELTA          = .05 

class FamilyAgent(Agent):
    """A family who chooses to attend a given school.

    A family contains the following parameters:
    - Wealth
    - Location (where they live on a 1 dimensional space)
    - Weighting of their priorities in choosing a school
    """
    def __init__(self, unique_id, model, 
                # Custom parameters
                wealth, 
                priorities,
                location):
        super().__init__(unique_id, model)
        self.wealth     = wealth
        self.location   = location
        self.priorities = priorities

    def score_school(self, school):
        """ Given a school and a family's parameters, return the utility score for that school.

        Input: A SchoolAgent

        Output: A numeric score for that score's perceived utility. Higher is better.
        """
        # Simple linear combination. Ensure scale of variables is comparable.
        # \/\/\/\/\//\/\/\/\/\/
        # Priorities: 0-1 scale
        # Prestige, Efficacy, and Tuition: N(0,1) random variables.
        score = (self.priorities['Prestige'] * school.prestige +
        	     self.priorities['Efficacy'] * school.efficacy - 
        	     self.priorities['Cost'] * school.tuition)
        # print('Priorities for family', self.unique_id, self.priorities['Prestige'], self.priorities['Efficacy'])
        return score

    def school_choice(self, wealth, location, priorities):
        """Score each school using `score_school` logic.
        
		Return the id of chosen school. 
        """
        schools= [obj for obj in self.model.schedule._agents.values() if isinstance(obj, SchoolAgent)]
        scores = [self.score_school(school) for school in schools]
        chosen_school = np.argmax(scores)
        return chosen_school

    def step(self):
        chosen_school = self.school_choice(self.wealth, self.location, self.priorities)
        
        # Give the chosen school some money.
        self.model.schedule.agents[chosen_school].endowment += self.model.schedule.agents[chosen_school].tuition
        # Take the tuition payment from this agent. 
        # Actually, not really relevant I don't think?
        # self.wealth -= self.model.schedule.agents[chosen_school].tuition

        # If the school is better than expected, future prestige goes up. Vice versa.
        # Maybe this makes families in future more open to low prestige schools, as
        # reputation spreads that schools with lower prestige can still provide good service?
        gap = (self.model.schedule.agents[chosen_school].efficacy - self.model.schedule.agents[chosen_school].prestige)
        if gap >= 0:  # Performance of school better than expected.
            self.model.schedule.agents[chosen_school].prestige += .5 * gap  # Prestige rises.
            # Also, make future families more amenable to prioritizing efficacy. Word spreads
            # that non-presitguous schools can be good, and more people open up to this.
            # They shouldn't just judge a school by its prestige.
            if self.model.family_priority_weights['Efficacy'] != 1:
            	if self.model.family_priority_weights['Prestige'] > WEIGHT_DELTA:
	            	self.model.family_priority_weights['Efficacy'] += WEIGHT_DELTA
	            	self.model.family_priority_weights['Prestige'] -= WEIGHT_DELTA
        else:  # Performance of school worse than expected.
            self.model.schedule.agents[chosen_school].prestige -= .5 * gap  # Prestige falls.
            # Families realize highly prestiguous schools might not help. So look for cost and efficacy.
            if ((self.model.family_priority_weights['Efficacy'] != 1) and (self.model.family_priority_weights['Cost'] != 1) ):
            	if self.model.family_priority_weights['Prestige'] > 2*WEIGHT_DELTA:
	            	self.model.family_priority_weights['Efficacy'] += WEIGHT_DELTA
	            	self.model.family_priority_weights['Cost']     += WEIGHT_DELTA
	            	self.model.family_priority_weights['Prestige'] -= 2*WEIGHT_DELTA

class SchoolAgent(Agent):
    def __init__(self, unique_id, model, 
        endowment, 
        prestige,
        tuition,
        annual_fund,
        efficacy,
        endowment_draw,
        priorities,
        location):
        super().__init__(unique_id, model)
        self.endowment      = endowment
        self.prestige       = prestige
        self.tuition        = tuition
        self.annual_fund    = annual_fund
        self.efficacy       = efficacy
        self.endowment_draw = endowment_draw
        self.priorities     = priorities
        self.location       = location

    def step(self):
        """
        How a school evolves over time.
        """
        # Endowment grows according to growth rate. 
        # Assume equal for all schools.
        self.endowment = self.endowment * (1 + ENDOWMENT_GROWTH_RATE)

        # Prestige can fall due to exongenous event (eg. sex scandal). 
        # TO DO: Make scandals of varying size and probability.
        possible_prestiges = [self.prestige, self.prestige*.75]
        draw = np.random.choice(possible_prestiges, 1, p=[1-SCANDAL_PROBABILITY, SCANDAL_PROBABILITY])
        # if possible_prestiges.index(draw) == 1:
            # print('School {} had a sex scandal! Old prestige was {} and new prestige is {}.'
                # .format(self.unique_id, self.prestige, self.prestige*.75))
        self.prestige = draw[0] 

        # print('family_priority_weights', self.model.family_priority_weights)
        # self.model.family_priority_weights = [i*.99 for i in self.model.family_priority_weights]

        return

