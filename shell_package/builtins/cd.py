import os
from shell_package.constants import *
# Creating our own cd command
def cd(args):
    os.chdir(args[0])
    return SHELL_STATUS_RUN
