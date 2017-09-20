import os
from os import path
import datetime as dt
from collections import namedtuple
import yaml
import click

""" Settings
"""
suffix = ' >> '
temp_dt = "%Y-%m-%d %H:%M:%S"

UIColor = namedtuple("color", "BOLD ERROR SUCCESS WARNING")
color = UIColor('\033[1m{}\033[0m',
                '\033[91m{}\033[0m',
                '\033[92m{}\033[0m',
                '\033[93m{}\033[0m')

soldi = color.BOLD.format("[Soldi]")

class Config(object):
    def __init__(self):
        self.soldi_config_dir = path.expanduser("~/.soldi")
        self.path_to_csv = "{0}/{1}".format(self.soldi_config_dir, "data/")
        self.path_to_figure = "{0}/{1}".format(self.soldi_config_dir, "figures/")

class ConfigChecker(Config):
    def __init__(self):
        super().__init__()

    def check(self):
        # Check whether a config directory exists.
        if not exist_config_dir():
            click.echo(soldi +
                       color.WARNING.format(" A config directory '~/.soldi' doesn't exist."))
            if make_config_dir():
                click.echo(soldi +
                           color.SUCCESS.format(" Successfully made configure directory."))
            else:
                click.echo(soldi +
                           color.ERROR.format(" Making configure directory was failure."))

        # Check whether a directory which store data csv exists in '~/.soldi'.
        if not path.isdir(self.path_to_csv):
            click.echo(soldi +
                       color.WARNING.format(" A directory which store data csv doesn't exist " \
                                            "in '~/.soldi' so Soldi will make that directory."))
            try:
                os.mkdir(self.path_to_csv)
                click.echo(soldi +
                           color.SUCCESS.format(" Successfully made configure directory."))
            except:
                click.echo(soldi +
                           color.ERROR.format(" Making configure directory was failure."))

        # Check whether a directory which store plot figures exists in '~/.soldi'.
        if not path.isdir(self.path_to_figure):
            click.echo(soldi +
                       color.WARNING.format(" A directory which store plot figures doesn't " \
                                            "exist in '~/.soldi' so Soldi will make that " \
                                            "directory."))
            try:
                os.mkdir(self.path_to_figure)
                click.echo(soldi +
                           color.SUCCESS.format(" Successfully made configure directory."))
            except:
                click.echo(soldi +
                           color.ERROR.format(" Making configure directory was failure."))

def exist_config_dir():
    soldi_config_dir = path.expanduser("~/.soldi")
    return path.isdir(soldi_config_dir)

def make_config_dir():
    soldi_config_dir = path.expanduser("~/.soldi")
    try:
        os.mkdir(soldi_config_dir)
        return True
    except:
        return False

def load_config(path_to_yaml):
    with open(path_to_yaml, 'r+') as stream:
        config = yaml.load(stream)
    return config

def what_is_the_date_today():
    """ return today's date
    """
    return dt.date.today()
