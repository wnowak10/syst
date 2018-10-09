# Imports 
# ______________________________________________________________________________

import numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation

# Constants 
# ______________________________________________________________________________

SCANDAL_PROBABILITY   = .03 # Use Choate as representative -- ~3/125 ~~ 3%
ENDOWMENT_GROWTH_RATE = .04 # Standard market returns. 


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
        """ Given a school and a Family's parameters, return the utility score for that school.
        """
        score = (self.priorities['Prestige']*school.prestige +
        	     self.priorities['Efficacy']*school.efficacy - 
        	     self.priorities['Cost']*school.tuition)
        # print('priorities for familiy', self.unique_id, self.priorities['Prestige'], self.priorities['Efficacy'])
        return score

    def school_choice(self, wealth, location, priorities):
        """ Score each school using `score_school` logic.
        Then return the id of chosen school. 
        """
        schools= [obj for obj in self.model.schedule._agents.values() if isinstance(obj, SchoolAgent)]
        scores = [self.score_school(school) for school in schools]
        chosen_school = np.argmax(scores)
        # print('Family {} chose school {}'.format(str(self.unique_id), str(chosen_school)))
        return chosen_school

    def step(self):
        chosen_school = self.school_choice(self.wealth, self.location, self.priorities)
        
        # TO DO: Does this really matter? E.g. do we want a family agent who persists?
        # It isn't so much the same family choosing again and again. 
        # Most families make these sorts of choices (boarding school, college)
         # 1-5x per lifetime. So keeping track of their decreasing wealth 
         # as a result of 1 payment is really not that important.
        # Maybe instead, at each step we just randomly generate new families each time
        # and the random parameters we initialize maybe change over time as families
        # generally change. TO DO: How do these parameters change?

        # Give the chosen school some money.
        self.model.schedule.agents[chosen_school].endowment += self.model.schedule.agents[chosen_school].tuition
        # Take the tuition payment from this agent. See above: not really relevant I don't think?
        # self.wealth -= self.model.schedule.agents[chosen_school].tuition

        # If the school is better than expected, future prestige goes up. Vice versa.
        # Maybe this makes families in future more open to low prestige schools, as
        # reputation spreads that schools with lower prestige can still provide good service?
        gap = (self.model.schedule.agents[chosen_school].efficacy - self.model.schedule.agents[chosen_school].prestige)
        if gap >= 0:
            self.model.schedule.agents[chosen_school].prestige += .5 * gap
        else:
            self.model.schedule.agents[chosen_school].prestige -= .5 * gap

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

        print('family_priority_weights', self.model.family_priority_weights)
        self.model.family_priority_weights = [i*.99 for i in self.model.family_priority_weights]

        return

