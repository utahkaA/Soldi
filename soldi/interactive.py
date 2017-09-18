# -*- coding: utf-8 -*-
import datetime as dt
import uuid
import pandas as pd
import click

from .table import *
from .utils import *

class Interactive(object):
    def __init__(self):
        self.inputed_event_records = pd.DataFrame(index=[], columns=Event().cols)

    def info(self):
        click.echo("=== Interactive Mode ===")
        click.echo("Insert data into soldi database based on your interactive input.")

    def prompt(self):
        event_prompt = EventPrompt()
        event_record = event_prompt.start()
        self.inputed_event_records = self.inputed_event_records.append(event_record,
                                                                       ignore_index=True)

        msg = "\n[Soldi] You can input receipt information of your inputed event."
        click.echo(msg)
        if click.confirm("Do you want to continue?"):
            receipt_prompt = ReceiptPrompt()
            receipt_record = receipt_prompt.start(event_record['_id'])

class EventPrompt(object):
    def __init__(self):
        self.definition = Event()

    def start(self):
        parsers = {
            '_timestamp': self._timestamp,
            '_where': self._where,
            '_howmuch': self._howmuch,
            '_kind': self._kind,
            '_from': self._from,
            '_to': self._to
        }
        record = dict()
        for col in self.definition.cols:
            if col in parsers:
                if not col in ['_from', '_to']:
                    record[col] = parsers[col]()
                    if col == '_kind':
                        msg = "\n[Soldi] Your inputed event record's kind is '{0}'" \
                              " so please its {0} information."
                        click.echo(msg.format(record['_kind']))
                else:
                    record[col] = parsers[col](record['_kind'])
            elif col in ['_created_at', '_updated_at']:
                record[col] = dt.datetime.now()
            elif col == '_id':
                record[col] = uuid.uuid4()

        return pd.Series(record, index=self.definition.cols)

    def _timestamp(self):
        msg = "input events._timestamp"
        _ts = click.prompt(msg, prompt_suffix=suffix, type=str)
        return dt.datetime.strptime(_ts, '%Y-%m-%d')

    def _where(self):
        msg = "input events._where"
        _where = click.prompt(msg, prompt_suffix=suffix, type=str)
        return _where

    def _howmuch(self):
        msg = "input events._howmuch"
        _howmuch = click.prompt(msg, prompt_suffix=suffix, type=int)
        return _howmuch

    def _kind(self):
        msg = "input events._kind (income/outgo/move)"
        _kind = click.prompt(msg, prompt_suffix=suffix, type=str)
        if not _kind in ['income', 'outgo', 'move']:
            msg = "your input is invalid value."
            raise click.UsageError(msg)
        return _kind

    def _from(self, kind):
        msg = "input events._from"
        _from = click.prompt(msg, prompt_suffix=suffix, type=str)

        if kind in ['outgo', 'move'] and not _from in ['wallet', 'local', 'bank']:
            msg = "your input is invalid value."
            raise click.UsageError(msg)

        return _from

    def _to(self, kind):
        msg = "input events._to"
        _to = click.prompt(msg, prompt_suffix=suffix, type=str)

        if kind in ['income', 'move'] and not _to in ['wallet', 'local', 'bank']:
            msg = "your input is invalid value."
            raise click.UsageError(msg)
        return _to

class ReceiptPrompt(object):
    def __init__(self):
        self.definition = Receipt()

    def start(self, event_id):
        parsers = {
            '_name': self._name,
            '_howmuch': self._howmuch
            '_howmany': self._howmany
        }
        inputed_records = pd.DataFrame(index=[], columns=self.definition.cols)
        while True:
            record = dict()
            for col in self.definition.cols:
                if col in parsers:
                    record[col] = parsers[col]()
                elif col in ['_created_at', '_updated_at']:
                    record[col] = dt.datetime.now()
                elif col == '_event_id':
                    record[col] = event_id
            record = pd.Series(record, index=self.definition.cols)
            inputed_records = inputed_records.append(record, ignore_index=True)
            if not click.confirm("Do you have other items yet?"):
                break
        return inputed_records

    def _name(self):
        msg = "input receipt._name"
        _name = click.prompt(msg, prompt_suffix=suffix, type=str)
        return _name

    def _howmuch(self):
        msg = "input receipt._howmuch"
        _howmuch = click.prompt(msg, prompt_suffix=suffix, type=int)
        return _howmuch

    def _howmany(self):
        msg = "input receipt._howmany"
        _howmany = click.prompt(msg, prompt_suffix=suffix, type=int)
        return _howmany
