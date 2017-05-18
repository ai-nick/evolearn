
import numpy as np
import itertools


def construct_substrate(resolution):

    if resolution == '5x5':

        nx, ny = 5, 5
        x = np.linspace(-1, 1, nx)
        y = np.linspace(-1, 1, ny)

        xv, yv = np.meshgrid(x, y)

        substrate_input = []
        substrate_hidden = []
        substrate_output = []

        for layer in range(nx):

            # Input
            if not layer:
                substrate_layer = zip(xv[layer], yv[layer])
                substrate_input.append(substrate_layer)
            # Hidden
            elif (layer > 0 ) and ( layer != nx-1):
                substrate_layer = zip(xv[layer], yv[layer])
                substrate_hidden.append(substrate_layer)
                # Output
            else:
                substrate_layer = zip(xv[layer], yv[layer])
                substrate_output.append(substrate_layer)


    return substrate_input[0], list(itertools.chain.from_iterable(substrate_hidden)), substrate_output[0]


resolution = '5x5'

i, h, o = construct_substrate(resolution)

print i, len(i)
print h, len(h)
print o, len(o)