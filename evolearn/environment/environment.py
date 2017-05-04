
import numpy as np
from animation import Animation
from agent import Agent
import matplotlib.pyplot as plt

class Environment:

    def __init__(self):

        self.num_decisions = 500

        self.visualize = False
        self.current = Simple(self.visualize)

    def run(self):

        self.current.reset(self.num_decisions)

        for decision in range(self.num_decisions):
            self.current.step()

        # print 'Cumulative Reward: ', self.current.agent.cumulative_reward

        if self.visualize:
            self.animate()

    def animate(self):

        anim = Animation(self.current.agent.world_history)
        anim.animate()

class Recognition:
    def __init__(self):
        pass

class Simple:

    def __init__(self, visualize):

        self.world_size = 100

        # Reward parameters
        self.variable_nutrients = True
        self.nutrient_density = .5
        self.metabolic_cost = -0.2
        self.nutrient_value = 3 * -1 * self.metabolic_cost
        self.world_vals = [ self.metabolic_cost, self.nutrient_value, visualize ]

    def reset(self, num_decisions):

        # Define a world with a certain nutrient density
        self.world = np.random.rand( self.world_size, self.world_size)

        self.world[self.world > self.nutrient_density] = 0

        if self.variable_nutrients:
            self.world = self.world / self.nutrient_density # normalize for density (and maximum values)
        else:
            self.world[ self.world > 0 ] = self.nutrient_value


        self.world[ self.world == 0 ] = self.metabolic_cost

        # Define an agent
        self.agent = Agent( self.world, num_decisions, self.world_vals )

    def step(self):

        self.agent.step()
#
# env = Environment()
# # env.run()
# decisions = [ 125, 250, 500, 1000, 2000 ]
#
# num_reps = 20
# densities = [ 0.15, 0.30, 0.45, 0.60, 0.75, 0.90 ]
#
# plot_count = 1
#
# for decisions in decisions:
#
#     print '-', decisions, 'Decisions'
#
#     env.num_decisions = decisions
#
#     cum_reward = np.zeros((num_reps, len(densities)))
#
#     for d in range(len(densities)):
#
#         print '     - Nutrient Density: ', densities[d]
#
#         env.current.nutrient_density = densities[d]
#
#         for rep in range(num_reps):
#
#             env.run()
#             cum_reward[rep, d] += env.current.agent.cumulative_reward
#
#     mean = np.mean(cum_reward, axis=0)
#     std = np.std(cum_reward, axis=0)
#     xaxis = np.zeros((len(densities), ))
#
#     plt.subplot(2, 3, plot_count)
#     plt.errorbar(densities, mean, yerr=std)
#     plt.plot(densities, xaxis)
#     plt.title(str(decisions) + ' Decisions')
#
#     plot_count += 1
#
# plt.show()