#!/usr/bin/env python
""" The main entry point.
"""
import click
from .table import *
from .interactive import *
from .plot import *
from .utils import *

@click.group()
def main():
    checker = ConfigChecker()
    checker.check()

def interactive_mode(debug):
    interactive = Interactive(debug)
    interactive.info()
    interactive.prompt()

@main.command()
@click.option("--debug", is_flag=True)
def insert(debug):
    interactive_mode(debug)

@main.command()
def sort():
    controller = TableController()
    controller.sort()

    msg = soldi + color.SUCCESS.format(" Tables were sorted successfully.")
    click.echo(msg)

@main.command()
def plot():
    resolution = 'D'
    plotter = Plotter(resolution)
    plotter.plot()

@main.command()
def show():
    controller = TableController()
    controller.show()
