
import MultiNEAT as mneat


params = mneat.Parameters()

dir = dir(params)

for i in dir:
    print i, getattr(params, i)