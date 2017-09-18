from os import path
import datetime as dt
import yaml

""" Settings
"""
suffix = ' >> '
temp_dt = "%Y-%m-%d %H:%M:%S"

def exist_config_dir():
    soldi_config_dir = path.expanduser("~/.soldi")
    return path.isdir(soldi_config_dir)

def load_config(path_to_yaml):
    with open(path_to_yaml, 'r+') as stream:
        config = yaml.load(stream)
    return config

def what_is_the_date_today():
    """ return today's date
    """
    return dt.date.today()
