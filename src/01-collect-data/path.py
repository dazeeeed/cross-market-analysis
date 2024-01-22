import os

def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_data_path_from_src():
    return os.path.abspath(os.path.join(get_current_path(), '../', 'data'))