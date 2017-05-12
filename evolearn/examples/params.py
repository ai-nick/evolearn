
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


import pkg_resources
import os
from pathlib2 import Path

class Parameters:

    """
    Parameter handing class.
    
    `Parameters` pulls from a specified .txt and saves variables in a dictionary to be used by a Simulation object.
    
    """

    def __init__(self, filename):

        # Define data path to the specified parameters file
        self.DATA_PATH = self.define_data_path(filename)

        # Callable dictionary of parameters to be passed
        self.values = self.params_txt_to_dict()

    def define_data_path(self, filename):

        # Check if the parameters file comes from the package examples

        if pkg_resources.resource_exists('evolearn.examples', 'params/' + filename):

            data_path = pkg_resources.resource_filename('evolearn.examples', 'params/' + filename)

        else:

            cwd = os.getcwd()
            dp_cwd_check = os.path.dirname(cwd) + '/' + filename
            check_path = Path(dp_cwd_check)

            # Check if the file exists in the current directory

            if check_path.exists():

                data_path = dp_cwd_check

            # Assume full path is specified.

            else:

                data_path = filename

        return data_path



    def params_txt_to_dict(self):

        dicts_from_file = {}

        # Read and build initial dictionary from file

        with open(self.DATA_PATH, 'r') as inf:

            for line in inf:

                # Ignore read on commented lines

                if not self.check_if_commented_line(line):

                    (key, val) = line.split(' = ')
                    val = val.strip('\n')

                    dicts_from_file[key] = self.restructure_param(val)

        return dicts_from_file

    def check_if_commented_line(self, s):

        output = False

        if s[0] == '#':

            output = True

        return output

    def check_if_int_string(self, s):

        # Test int function

        try:

            int(s)

            return True

        except ValueError:

            return False

    def restructure_param(self, val):

        # Test bool

        if val[0] == '*':

            if val[1] == 'T':

                new_value = True

            else:

                new_value = False

        # Test int

        elif self.check_if_int_string(val[0]):

            try:


                new_value = int(val)

            except:

                new_value = float(val)

        # Else string

        else:

            new_value = val

        return new_value

