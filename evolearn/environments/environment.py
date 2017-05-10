
#######################################################
#   ____  _      ___   _     ____   __    ___   _     #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ | #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \| #
#                                                     #
#                  Chad Carlson - 2017                #
#######################################################



from evolearn.controllers.controller import SimpleAgent

import numpy as np


class SimpleEnvironment:

    """
    Simple wrapped callable nutrient environment.
    
    Todo:
        * Allow for the import of txt file for defining maze/track boundaries.
    """

    def __init__(self):

        # Environment parameters
        self.world_size = 100
        self.walls = False

        # Reward parameters
        self.variable_nutrients = False
        self.nutrient_density = .25

        self.metabolic_cost = -0.2

        self.nutrient_relative_to_cost = 3
        self.nutrient_value = self.nutrient_relative_to_cost * -1 * self.metabolic_cost

        # Agent parameters
        self.observation_space = 9
        self.action_space = 5

        # Possible actions in environment
        self.actions = self.build_actions()

        # Define Agent object
        self.agent = SimpleAgent()

    def build_actions(self):

        # Position adjustments
        empty_position_adjust = [ [0,0], [0,0], [0,0], [0,0] ]
        straight = [ [-1,0], [0,1], [1,0], [0,-1] ]
        diagonal_right = [ [-1,1], [1,1], [1,-1], [-1,-1] ]
        diagonal_left = [ [-1,-1], [-1,1], [1,1], [1,-1] ]

        actions = {}

        # Position changes
        actions[0] = { 'heading_adjust': 0, 'position_adjust': straight }
        actions[1] = { 'heading_adjust': 0, 'position_adjust': diagonal_right }
        actions[2] = { 'heading_adjust': 0, 'position_adjust': diagonal_left }

        # Heading changes
        actions[3] = { 'heading_adjust': -1, 'position_adjust': empty_position_adjust }
        actions[4] = { 'heading_adjust': 1, 'position_adjust': empty_position_adjust }

        return actions

    def reset(self):

        """
        Complete environment reset.
        
        :return: intial environment observation
        """

        # Define a world with a certain nutrient density
        self.world = np.random.rand( self.world_size, self.world_size)
        self.world[self.world > self.nutrient_density] = 0

        if self.variable_nutrients:
            self.world = self.world / self.nutrient_density # normalize for density (and maximum values)
        else:
            self.world[ self.world > 0 ] = self.nutrient_value

        self.world[ self.world == 0 ] = self.metabolic_cost

        # Initialize your agent
        self.agent.reset(self.world_size)

        return self.make_observation()

####################### may make more sense if enforce_wrapping and cyclical_heading are in the SimpleAgent controller class

    def enforce_wrapping(self, position):

        """
        Location conversion. Prevents requests for locations that are not pre-allocated.
        
        :param: world positionX or world positionY
        :return: new world positionX or world positionY
        
        """

        if position >= self.world_size:
            wrapped_position = 0
        elif position < 0:
            wrapped_position = self.world_size - 1
        else:
            wrapped_position = position

        return wrapped_position


    def cyclical_heading(self, heading):

        """
        Heading conversion. Prevents requests for heading indices that do not exist ( range(4) possible ).

        :param: original agent.heading
        :return: converted (cyclical) agent.heading

        """

        if heading < 0:
            heading = 3
        elif heading > 3:
            heading = 0

        return heading


    def collision_check(self):

        """
        Collision check to potentially break current agent's evaluation.
        
        :return: collide Boolean 
        """

        if self.walls:
            if self.world[ self.agent.location[0], self.agent.location[1] ] > self.nutrient_value:
                collide = True
        else:
            collide = False

        return collide


    def update(self, action):

        """
        Update environment.world with respect possibly consumed nutrients at agent's current location.
        
        :return: None
        
        """

        self.world[ self.agent.location[0], self.agent.location[1] ] = self.metabolic_cost

#######################
    def move_agent(self, action):

        """
        Update agent location based on selected action.
        
        :return: None 
        """


    def return_reward(self):

        """
        Reward return for occupied location.
        
        :return: reward/state at agent.location 
        """

        return self.world[ self.agent.location[0], self.agent.location[1] ]

#######################
    def make_observation(self):

        """
        Making an observation in a single step through environment.
        """

        pass


    def reformat_action(self, agent_output):

        """
        Reformat raw network output into environment-specific (or experiment specified) action/class choice.
         
        :return: reformatted action/class index
        """
        action = agent_output.index( max(agent_output) )

        return action


    def step(self, action):

        """
        Making a single step through the environment. 
        """

        self.update(action)

        observation = self.make_observation()

        state = self.return_reward()

        collide = self.collision_check()

        return observation, state, collide



    # def define_FOV(self):
    #
    #     rows = range(self.location[0] - (self.levels_FOV), self.location[0] + (self.levels_FOV + 1))
    #     cols = range(self.location[1] - (self.levels_FOV), self.location[1] + (self.levels_FOV + 1))
    #
    #     FOV = list(itertools.product(rows, cols))
    #     FOV = [(self.enforce_wrapping(i), self.enforce_wrapping(j)) for i, j in FOV]
    #
    #     FOV_heading = self.define_FOV_heading()
    #
    #     final_FOV = [ FOV[i] for i in FOV_heading ]
    #
    #     observation = np.array( [ self.world[ point[0], point[1] ] for point in final_FOV ])
    #
    #     if self.visualize:
    #         self.visualize_FOV(final_FOV)
    #
    #     return observation
    #
    # def define_FOV_heading(self):
    #
    #     FOV_heading = []
    #     r = 2 * self.levels_FOV + 1
    #     tH = self.levels_FOV * r
    #     t = r ** 2
    #
    #     for l in range(1, self.levels_FOV + 1):
    #
    #         if not self.heading:  # Heading = 0
    #             FOV_heading += range((self.levels_FOV - l) * r, (self.levels_FOV - l + 1) * r, 1)
    #
    #         elif self.heading == 1:  # Heading = 1
    #             FOV_heading += range(r - (self.levels_FOV - l + 1), t, r)
    #
    #         elif self.heading == 2:  # Heading = 2
    #             FOV_heading += range((r - (self.levels_FOV - l)) * r - 1, (self.levels_FOV + l) * r - 1, -1)
    #
    #         elif self.heading == 3:  # Heading = 3
    #             FOV_heading += range(2 * tH + (self.levels_FOV - l), self.levels_FOV - l - 1, -1 * r)
    #
    #     return FOV_heading
    #
    # def visualize_FOV(self, FOV):
    #     for receptor in FOV:
    #         self.world_history[ receptor[0], receptor[1], self.step_tick - 1 ] = 0.75 * self.agent_value
    #
    # def act(self, observation):
    #
    #     # Execute a random action
    #     action = self.actions[np.random.randint(self.action_space)]
    #
    #     # Update heading
    #     self.heading = self.cyclical_heading( self.heading + action['heading_adjust'] )
    #
    #     # Update location
    #     self.location[0] = self.enforce_wrapping( self.location[0] + action['position_adjust'][self.heading][0] )
    #     self.location[1] = self.enforce_wrapping( self.location[1] + action['position_adjust'][self.heading][1] )
    #
    #     # Update the cumulative reward for the agent's new location
    #     self.cumulative_reward += self.world[ self.location[0], self.location[1] ]
    #
    # def observe(self):
    #
    #     # Define the agent FOV
    #     observation = self.define_FOV()
    #
    #     return observation
    #
    # def step(self):
    #
    #     if not (self.step_tick > (self.num_decisions - 1)):
    #
    #         if not (self.step_tick > (self.num_decisions - 2)) and self.visualize:
    #
    #             # Copy the current world to the subsequent frame
    #             self.world_history[:, :, (self.step_tick + 1)] = copy(self.world)
    #
    #         # Perform an observation
    #         observation = self.observe()
    #
    #         # Act on that observation
    #         self.act(observation)
    #
    #         # Remove consumed nutrients
    #         self.world[self.location[0], self.location[1]] = self.metabolic_cost
    #
    #         if self.visualize:
    #             # Draw the agent onto the world
    #             self.world_history[self.location[0], self.location[1], self.step_tick] = self.agent_value
    #
    #     self.step_tick += 1


class Recognition:

    """
    General image recognition object.
    """
    def __init__(self):
        pass

