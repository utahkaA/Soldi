# -*- coding: utf-8 -*-
from os import path
import datetime as dt
import uuid
import pandas as pd
import click

from .table import *
from .utils import *

class Interactive(Config):
    def __init__(self, is_debug=False):
        super().__init__()
        self.inputed_event_records = pd.DataFrame(index=[], columns=Event().cols)
        self.inputed_receipt_records = pd.DataFrame(index=[], columns=Receipt().cols)
        self.is_debug = False if is_debug else True

    def info(self):
        addition = "(Debug) " if not self.is_debug else ""
        click.echo("=== Interactive Mode " + addition + "===")
        click.echo("Insert data into soldi database based on your interactive input.")

    def _writeout(self, df, csv_name):
        path_to_csv = self.path_to_csv + csv_name + ".csv"

        ## Write out a dataframe.
        if path.isfile(path_to_csv):
            with open(path_to_csv, 'a') as stream:
                df.to_csv(stream, index=False, header=False)
        else:
            df.to_csv(path_to_csv, index=False, header=True)

    def _receipt_prompt(self, event_record):
        receipt_prompt = ReceiptPrompt()
        receipt_record = receipt_prompt.start(event_record['_id'])

        if self._check_receipt_content(event_record, receipt_record):
            # Append a record to receipt dataframe.
            self.inputed_receipt_records = pd.concat([self.inputed_receipt_records,
                                                      receipt_record],
                                                      ignore_index=True)
            return True
        else:
            return False

    def _check_receipt_content(self, event_record, receipt_record):
        # Check receipt data
        howmany_ser = receipt_record._howmany
        howmuch_ser = receipt_record._howmuch
        receipt_sum = (howmany_ser * howmuch_ser).sum()
        if event_record._howmuch == receipt_sum:
            click.echo(soldi + \
                       color.SUCCESS.format(" Registered receipt data successfully."))
            return True

        elif event_record._howmuch > receipt_sum:
            warning_msg = soldi + color.WARNING.format(" The amount of inputted " \
                          "receipt is smaller than that of event data. Would you " \
                          "like to register with this content?")
            if not click.confirm(warning_msg):
                click.echo(soldi + \
                           " Okay then, Could you input again?")
                return False
            else:
                click.echo(soldi + \
                           color.SUCCESS.format(" Registered receipt data."))
                return True
        else:
            error_msg = soldi + color.ERROR.format(" The amount of inputted " \
                        "receipt is larger than that of event data.")
            click.echo(error_msg)
            click.echo(soldi + \
                       " Could you input again?")
            return False

    def prompt(self):
        while True:
            event_prompt = EventPrompt()
            event_record = event_prompt.start()
            self.inputed_event_records = self.inputed_event_records.append(event_record,
                                                                           ignore_index=True)
            # Input receipt information.
            if event_record['_kind'] == "outgo":
                msg = "\n" + soldi + \
                      " You can input receipt information of your inputed event."
                click.echo(msg)
                if click.confirm(soldi + " Do you want to continue?"):
                    while True:
                        status = self._receipt_prompt(event_record)
                        if status:
                            break

                        # receipt_prompt = ReceiptPrompt()
                        # receipt_record = receipt_prompt.start(event_record['_id'])
                        #
                        # # Check receipt data
                        # howmany_ser = receipt_record._howmany
                        # howmuch_ser = receipt_record._howmuch
                        # receipt_sum = (howmany_ser * howmuch_ser).sum()
                        # if event_record._howmuch == receipt_sum:
                        #     # Append a record to receipt dataframe.
                        #     self.inputed_receipt_records = pd.concat([self.inputed_receipt_records,
                        #                                               receipt_record],
                        #                                               ignore_index=True)
                        #     click.echo(soldi + \
                        #                color.SUCCESS.format(" Registered receipt data successfully"))
                        # elif event_record._howmuch > receipt_sum:
                        #     warning_msg = soldi + color.WARNING.format(" The amount of inputted " \
                        #                   "receipt is smaller than that of event data. Would you " \
                        #                   "like to register with this content?")
                        #     if not click.confirm(warning_msg):
                        #         # もう一度レシートデータを登録するようにするべき
                        #         break
                        #     else:
                        #         # Append a record to receipt dataframe.
                        #         self.inputed_receipt_records = pd.concat([self.inputed_receipt_records,
                        #                                                   receipt_record],
                        #                                                   ignore_index=True)
                        # else:
                        #     error_msg = soldi + color.ERROR.format(" The amount of inputted " \
                        #                 "receipt is larger than that of event data.")
                        #     click.echo(error_msg)
                        #     break

            if not click.confirm("\n" + soldi + " Would you like to register other event data?"):
                break

        # Write out dataframes.
        if self.is_debug:
            ## Write out a event dataframe.
            self._writeout(self.inputed_event_records, "event")

            ## Write out a receipt dataframe.
            self._writeout(self.inputed_receipt_records, "receipt")


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
                        msg = "\n" + soldi + " Your inputed event record's kind is '{0}'" \
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
        while True:
            msg = "input events._timestamp"
            _ts = click.prompt(msg, prompt_suffix=suffix, type=str)

            try:
                return pd.to_datetime(_ts)
            except:
                click.echo(soldi + color.WARNING.format(" Could you input timestamp again?" \
                           "Its format is 'yyyy-mm-dd HH:MM:SS', 'yyyy/mm/dd HH:MM:SS'" \
                           " and so on."))

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
            '_howmuch': self._howmuch,
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

            # Confirmation of registration.
            if click.confirm(soldi + " Would you like to register with this content?"):
                record = pd.Series(record, index=self.definition.cols)
                inputed_records = inputed_records.append(record, ignore_index=True)
            # Whether to continue resitering.
            if not click.confirm(soldi + " Do you have other items yet?"):
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
