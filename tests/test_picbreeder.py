###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################

from evolearn.applications import PicBreeder


if __name__ == '__main__':

    pb = PicBreeder
    pb.run()
