
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
from evolearn.applications.interactive_evolution.kv_builder import SelectMultipleBuilder

# # Build the PicBreeder Application
#
pb = PicBreeder()

# Run the Application

pb.run()
#
# sm = SelectMultipleBuilder()
# print sm.return_string