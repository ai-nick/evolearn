
import numpy as np
import matplotlib.pyplot as plt

class WalledEnvironment:

    def __init__(self):

        self.world_size = 50

        self.nutrient_density = .4

        self.metabolic_cost = -0.25

        self.nutrient_relative_to_cost = 4
        self.nutrient_value = self.nutrient_relative_to_cost * -1 * self.metabolic_cost

        self.world = self.build_world()

        self.walls = True
        self.wall_width = int(round(0.025*self.world_size))
        self.wall_value_relative_to_nutrients = 5
        self.wall_value = self.wall_value_relative_to_nutrients * self.nutrient_value

        self.build_walls()

    def build_world(self):

        world = np.zeros((self.world_size, self.world_size))
        world[world > self.nutrient_density] = 0
        world[world > 0] = self.nutrient_value
        world[world == 0] = self.metabolic_cost

        return world

    def build_walls(self):

        self.build_border_box()

    def build_border_box(self):

        self.world[:, 0:self.wall_width] = self.wall_value * np.ones((self.world_size, self.wall_width))
        self.world[0:self.wall_width, :] = self.wall_value * np.ones((self.wall_width, self.world_size))
        self.world[:, self.world_size - self.wall_width:] = self.wall_value * np.ones((self.world_size, self.wall_width))
        self.world[self.world_size - self.wall_width:, :] = self.wall_value * np.ones((self.wall_width, self.world_size))

    def show(self):

        plt.imshow(self.world)
        plt.show()