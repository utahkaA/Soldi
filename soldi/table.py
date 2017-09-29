# -*- coding: utf-8 -*-
from datetime import datetime

import pandas as pd

from .utils import *

class Event(object):
    def __init__(self):
        self.cols = ['_id',
                     '_timestamp',
                     '_where',
                     '_howmuch',
                     '_kind',
                     '_from',
                     '_to',
                     '_created_at',
                     '_updated_at']

class Receipt(object):
    def __init__(self):
        self.cols = ['_event_id',
                     '_name',
                     '_howmany',
                     '_howmuch',
                     '_created_at',
                     '_updated_at']

class TableController(Config):
    def __init__(self):
        super().__init__()

        self.path_to_event = self.path_to_csv + "event.csv"
        self.path_to_receipt = self.path_to_csv + "receipt.csv"

        self.event_df = pd.read_csv(self.path_to_event)
        self.receipt_df = pd.read_csv(self.path_to_receipt)

    def sort(self):
        ts = datetime.now().strftime("%Y-%m-%d")
        path_to_bak_csv = self.path_to_bak + "event_{0}.csv".format(ts)
        self.event_df.to_csv(path_to_bak_csv, index=False, header=True)

        self.event_df = self.event_df.sort_values(by="_timestamp").reset_index(drop=True)
        self.event_df.to_csv(self.path_to_event, index=False, header=True)
