

###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################

from evolearn.applications.interactive_evolution.image_test import ImageTest

img = ImageTest()

print img.images_normal
print img.images_pressed