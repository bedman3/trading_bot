import os


def get_debug_from_env() -> bool:
    debug_env = os.environ.get("DEBUG", False)
    if isinstance(debug_env, bool):
        return debug_env
    elif isinstance(debug_env, str) and debug_env.lower() == 'true':
        return True
    return False
