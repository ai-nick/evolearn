
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


import pkg_resources


class Parameters:

    """
    Parameter handing class.
    
    `Parameters` pulls from a specified .txt and saves variables in a dictionary to be used by a Simulation object.
    
    Todo:
        * Allow handling filepaths of arbitrary location specified by user (os.path.join()?).
    """

    def __init__(self, filename):

        # Define data path to the specified parameters file
        self.DATA_PATH = pkg_resources.resource_filename('evolearn.examples', 'params/' + filename)

        # Callable dictionary of parameters to be passed
        self.values = self.params_txt_to_dict()

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

            new_value = int(val)

        # Else string

        else:

            new_value = val

        return new_value

