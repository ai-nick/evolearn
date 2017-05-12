
import itertools


def neighbors(point):

    x, y = point
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x + 1, y - 1
    yield x - 1, y + 1
    yield x - 1, y - 1

def advance(board):
    newstate=set()
    recalc = board | set(itertools.chain(*map(neighbors, board)))
    for point in recalc:
        count = ((neigh in board) for neigh in neighbors(point))
        if count == 3 or (count == 2 and point in board):
            newstate.add(point)
    return newstate

glider = set([(0, 0), (1,0), (2, 0), (0, 1), (1, 2)])

print advance(glider)

# for i in range(100):
#     print i
#     glider = advance(glider)
# print glider