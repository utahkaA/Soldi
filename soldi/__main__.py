#!/usr/bin/env python
""" The main entry point.
"""
import yaml
import click
from .table import *
from .interactive import *
from .utils import *


@click.group()
def main():
    checker = ConfigChecker()
    checker.check()

def interactive_mode():
    interactive = Interactive()
    interactive.info()
    interactive.prompt()

@main.command()
def insert():
    interactive_mode()
