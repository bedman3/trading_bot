import os
import sys


def get_debug_from_env() -> bool:
    """
    check if the application is run in debug mode
    """
    debug_env = os.environ.get("DEBUG", False)
    if isinstance(debug_env, bool):
        return debug_env
    elif isinstance(debug_env, str) and debug_env.lower() == 'true':
        return True
    return False


def in_pytest() -> bool:
    """
    check it the execution is under pytest testing framework
    """
    return 'pytest' in sys.modules
