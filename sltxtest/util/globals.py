import copy
import logging

import sltxpkg.globals as sg
# Deep copy the configuration
from sltxpkg import heart
from sltxpkg.log_control import LOGGER

configuration = copy.deepcopy(sg.configuration)


def restore_configuration():
    """Restores the global configuration
    """
    sg.configuration = copy.deepcopy(configuration)


def run_bare_sltx(args: list):
    """Runs sltx
    """
    LOGGER.setLevel(logging.ERROR)
    heart.run(args)
