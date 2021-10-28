#################################################
#
# @Author: davidecolombo
# @Date: dom, 24-10-2021, 20:36
# @Description: this script defines the main function for the 'initialize' module

#               This module is used for loading for the first time the sensor's data to the
#
#################################################
import sys
import time
from typing import List
import airquality.constants.system_constants as sc
from airquality.bot.initialize_bot import InitializeBotFactory
from airquality.constants.shared_constants import VALID_PERSONALITIES, DEBUG_HEADER, INITIALIZE_USAGE


def parse_sys_argv(args: List[str]):

    is_personality_set = False
    is_api_address_number_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            sc.DEBUG_MODE = True
        elif arg in VALID_PERSONALITIES and not is_personality_set:
            sc.PERSONALITY = arg
            is_personality_set = True
        elif arg.isdigit() and not is_api_address_number_set:
            sc.API_ADDRESS_N = arg
            is_api_address_number_set = True
        else:
            print(f"{parse_sys_argv.__name__}(): ignoring invalid option '{arg}'")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing personality argument. \n{INITIALIZE_USAGE}")

    if not is_api_address_number_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required api address number.")


################################ MAIN FUNCTION INITIALIZE MODULE ################################
def main():
    """This function is the entry point for the 'initialize' module.

    The module allows to set up all the information associated to the sensors and add them to the database."""

    args = sys.argv[1:]
    if not args:
        raise SystemExit(f"{main.__name__}: missing required argument. {INITIALIZE_USAGE}")

    parse_sys_argv(args)
    print(f"{DEBUG_HEADER} personality = {sc.PERSONALITY}")
    print(f"{DEBUG_HEADER} debug       = {sc.DEBUG_MODE}")

    try:
        start_time = time.perf_counter()
        print(20*'-' + " START THE PROGRAM " + 20*'-')
        initialize_bot = InitializeBotFactory().create_initialize_bot(bot_personality = sc.PERSONALITY)
        initialize_bot.run()
        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
        end_time = time.perf_counter()
        print(f"{DEBUG_HEADER} total time = {end_time - start_time}")

    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
