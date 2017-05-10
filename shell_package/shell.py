import os
import sys
import shlex
from shell_package.constants import *
from shell_package.builtins import *

# Dict to store our builtins and references
builtins = {}

# Add a built in command into our map
def add_command(name, action):
    builtins[name] = action

# Register the builtins
def init():
    add_command("cd", cd)
    add_command("exit", exit)
    add_command("#", comment)

def tokenize(command):
    return shlex.split(command)

def execute(command):
    # Get command name and arguments
    cmd_n = command[0]
    cmd_a = command[1:]

    # Check if its in our builtins Dict
    if cmd_n in builtins:
        return builtins[cmd_n](cmd_a)
    # Execute the command
    pid = os.fork()
    if pid == 0:
        # Child process
        os.execvp(command[0], command)
    elif pid > 0:
        # we're the parent so wait on our Child
        while True:
            wpid, status = os.waitpid(pid, 0)

            # Finish waiting if child exits regularly
            if os.WIFEXITED(status) or os.WIFSIGNALED(status): break

    return SHELL_STATUS_RUN

# Where the looping for the shell stuff happens
def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        # write out the >
        sys.stdout.write('> ')
        sys.stdout.flush()

        # Read the users input
        cmd = sys.stdin.readline()

        # Tokenize the command
        cmd_t = tokenize(cmd)

        # Execute and get new status
        status = execute(cmd_t)




def main():
    init()
    shell_loop()

if __name__ == '__main__':
    main()
