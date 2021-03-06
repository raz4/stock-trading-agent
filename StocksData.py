import csv
import collections
import numpy as np
from dateutil.parser import parse

Prices = collections.namedtuple('Prices', field_names=['date', 'open', 'high', 'low', 'close', 'volume'])

def read_csv(file_name, sep=',', filter_data=True, fix_open_price=False):
    with open(file_name, 'rt') as fd:
        reader = csv.reader(fd, delimiter=sep)
        h = next(reader)
        indices = [h.index(s) for s in ('open','high','low','close','volume')]
        date_index = h.index('date')
        d, o, h, l, c, v = [], [], [], [], [], []
        for row in reader:
            vals = list(map(float, [row[idx].replace(',', '') for idx in indices]))
            po, ph, pl, pc, pv = vals
            d.append(format_date(row[date_index]))
            o.append(po)
            c.append(pc)
            h.append(ph)
            l.append(pl)
            v.append(pv)
    return Prices(date=np.array(d, dtype=np.str),
                  open=np.array(o, dtype=np.float32),
                  high=np.array(h, dtype=np.float32),
                  low=np.array(l, dtype=np.float32),
                  close=np.array(c, dtype=np.float32),
                  volume=np.array(v, dtype=np.float32))

def prices_to_relative(prices):
    """
    Convert prices to relative in respect to open price
    :param ochl: tuple with open, close, high, low
    :return: tuple with open, rel_close, rel_high, rel_low
    """
    assert isinstance(prices, Prices)
    rh = (prices.high - prices.open) / prices.open
    rl = (prices.low - prices.open) / prices.open
    rc = (prices.close - prices.open) / prices.open
    return Prices(open=prices.open, high=rh, low=rl, close=rc, volume=prices.volume)

def format_date(date):
    """
    Convert a generic date into ISO 8601 date format
    :param date: generic date
    :return: date in ISO 8601 format
    """
    d = parse(date)
    return str(d.year) + "-" + ("0" if d.month < 10 else "") + str(d.month) + "-" + ("0" if d.day < 10 else "") + str(d.day)
