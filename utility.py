def does_module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    return True
