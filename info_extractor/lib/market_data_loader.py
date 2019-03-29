import os
import pandas as pd

def get_data_loader(market):
    data_loaders = {
        'NZX': NZX_load_data
    }
    return data_loaders[market]


def NZX_load_data(market):
    # TODO
    # raw_data = pd.read_csv('')
    pass


def data_saver_csv(file, market, filename):
    if not os.path.exists("static/file_store/market_data/%s/" % (market,)):
        os.makedirs("static/file_store/market_data/%s/" % (market,))

    with open("static/file_store/market_data/%s/%s.csv" % (market, filename), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)