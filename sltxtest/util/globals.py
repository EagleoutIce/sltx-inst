import copy

import sltxpkg.globals as sg
# Deep copy the configuration

configuration = copy.deepcopy(sg.configuration)


def restore_configuration():
    """Restores the global configuration
    """
    sg.configuration = copy.deepcopy(configuration)


def run_bare_sltx(args: list):
    """Runs sltx
    """
