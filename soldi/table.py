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
