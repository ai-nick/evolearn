
import numpy as np


class Activation:

    '''
    Activation Function class to be called for any particular network node.
    '''

    def __init__(self):
        self.remove_list = ['__init__', '__doc__', '__module__', 'remove_list']
        self.tags = list( set( dir( self ) ) - set( self.remove_list ) )

    # Absolute Value
    def abs_value(self, input):
        return np.abs(input)

    # Sigmoid
    def sigmoid(self, input):
        return 1 / ( 1 + np.exp(-1*input))

    # Gaussian
    def gauss(self, input):
        return np.exp(-input**2/2)

    # Linear
    def linear(self, input):
        return input

    # Sine
    def sine(self, input):
        return np.sin(input)

    # Step
    def step(self, input):
        return np.sign(input)

    # Ramp
    def ramp(self, input):
        return np.maximum(input, 0)

    # X-Cubed
    def x_cubed(self, input):
        return input ** 3

    # Tanh
    def tan_h(self, input):
        return np.tanh(input)

    # Rectified Linear Unit
    def ReLU(self, input):
        return max( [ input, 0 ] )

