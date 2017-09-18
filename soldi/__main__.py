#!/usr/bin/env python
""" The main entry point.
"""
import yaml
import click
from .transition import MoneyTransition
from .table import *
from .interactive import *
from .utils import *

@click.group()
def main():
    print("Hello, Soldi")


def interactive_mode():
    interactive = Interactive()
    interactive.info()
    interactive.prompt()

@main.command()
def insert():
    interactive_mode()
