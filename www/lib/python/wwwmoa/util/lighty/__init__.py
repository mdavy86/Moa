####################
### WWWMoaLighty ###
####################

import sys
sys.path.append("../../../")

from prompt import print_sys_message
from prompt import print_error_message
from prompt import print_message
from prompt import do_main_prompt
from prompt import do_prompt
from prompt import do_bool_prompt
from prompt import do_int_prompt

from help import show_help

from inst import show_status
from inst import schedule_cleanup
from inst import _inst as instances

from wizard import do_run_wizard
from wizard import do_kill_wizard

import os
import os.path
import subprocess
import random
import threading
import time







def execute_command(command):

    if command=="":
        print_sys_message("Sorry, but you did not type a command.")
    elif command=="h" or command=="help" or command=="?":
        show_help()
    elif command=="s" or command=="status":
        show_status()
    elif command=="r" or command=="run":
        do_run_wizard()
    elif command=="k" or command=="kill":
        do_kill_wizard()
    elif command=="q" or command=="quit" or command=="exit":
        pass
    else:
        print_error_message("The command you typed is not recognized.")








print """
## WWWMoaLighty
## lighttpd Manager for WWWMoa

""",



print_sys_message("Welcome!")

schedule_cleanup()



command=""
while True:
    if command=="q" or command=="quit" or command=="exit":
        if len(instances)>0:
            print_sys_message("You still have instances running.")
            term_conf=do_bool_prompt("Do you want to terminate all currently running instances? You will not be able to exit from WWWMoaLighty until they have been terminated.")
            if term_conf:
                for i in instances:
                    i["process"].terminate()

                while len(instances)>0:
                    time.sleep(1)

                print_sys_message("All instances have been terminated.")
                break
            else:
                print_sys_message("You have opted not to terminate all currently running instances.")
        else:
            break

    command=do_main_prompt().strip()

    execute_command(command)


print_sys_message("Goodbye!")

sys.exit(0);