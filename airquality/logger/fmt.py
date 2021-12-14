######################################################
#
# Author: Davide Colombo
# Date: 13/11/21 17:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging

GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"

COLORED_LEVELS = {'DEBUG': GREEN, 'INFO': BLUE, 'WARNING': YELLOW, 'ERROR': RED}
FORMAT_STRING = f"%(levelname)-20s %(asctime)-25s %(message)s"


################################ get_formatter_cls() ################################
def get_formatter(use_color=False):
    return ColoredFormatter(fmt=FORMAT_STRING) if use_color else CustomFormatter(fmt=FORMAT_STRING)


# ------------------------------- CustomFormatter ------------------------------- #
class CustomFormatter(logging.Formatter):
    """Custom formatter for changing the name of the file and calling function (used in the 'log_decorator')."""

    def format(self, record) -> str:
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override
        return super(CustomFormatter, self).format(record)


# ------------------------------- ColoredFormatter ------------------------------- #
class ColoredFormatter(logging.Formatter):

    def format(self, record) -> str:
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override

        levelname = record.levelname
        if levelname in COLORED_LEVELS:
            colored_levelname = COLORED_LEVELS[levelname] + levelname + RESET
            record.levelname = colored_levelname
        return super(ColoredFormatter, self).format(record)
