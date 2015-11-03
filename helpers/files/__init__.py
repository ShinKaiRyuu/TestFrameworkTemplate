import os


def get_full_path(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename) if filename else ''
