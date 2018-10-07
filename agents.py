# Imports 
# ______________________________________________________________________________

import numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation

# Constants 
# ______________________________________________________________________________

SCANDAL_PROBABILITY = .05
ENDOWMENT_GROWTH_RATE = .04 


class FamilyAgent(Agent):
    """ An family contains the following parameters:

    - Wealth
    - Location (where they live on a 1 dimensional space)
    - Weighting of their priorities in choosing a school
    """
    def __init__(self, unique_id, model, 
                # Custom parameters
                wealth, 
                priority,
                location):
        super().__init__(unique_id, model)
        self.wealth   = wealth
        self.location = location
        self.priority = priority

    def score_school(self, school):
        """ Given a school and a Family's parameters, return the utility score for that school.
        """
        print(self.priority)
        print(self.unique_id)
        print('prestige', school.prestige)
        print('endowment', school.endowment)
        if self.priority == 'prestige':
            return school.prestige
        else:
            return school.endowment

    def school_choice(self, wealth, location, priority):
        """ Score each school using `score_school` logic.
        Then return the id of chosen school. 
        """
        schools= [obj for obj in self.model.schedule._agents.values() if isinstance(obj, SchoolAgent)]
        scores = [self.score_school(school) for school in schools]
        chosen_school = np.argmax(scores)
        print('chose school is :', chosen_school)
        return chosen_school

    def step(self):
        chosen_school = self.school_choice(self.wealth, self.location, self.priority)
        
        # TO DO: Does this really matter? It isn't so much the same 
        # family choosing again and again. Most families make these sorts of choices
        # (boarding school, college) 1-5x per lifetime. So keeping track of their 
        # decreasing wealth as a result of 1 payment is really not that important.

        # Maybe instead at each step we just randomly generate new families each time
        # and the random parameters we initialize maybe change over time as families
        # generally change. 
        # Give the chosen school some money.
        self.model.schedule.agents[chosen_school].endowment += self.model.schedule.agents[chosen_school].tuition
        # Take the tuition payment from this agent.
        self.wealth -= self.model.schedule.agents[chosen_school].tuition

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
        possible_prestiges = [self.prestige, self.prestige*.75]
        draw = np.random.choice(possible_prestiges, 1, p=[1-SCANDAL_PROBABILITY, SCANDAL_PROBABILITY])
        if possible_prestiges.index(draw) == 1:
            print('School {} had a sex scandal! Old prestige was {} and new prestige is {}.'
                .format(self.unique_id, self.prestige, self.prestige*.75))
        self.prestige = draw[0] 

        return

