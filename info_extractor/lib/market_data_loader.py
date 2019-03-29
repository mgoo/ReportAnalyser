import os
import pandas as pd

def get_data_loader(market):
    data_loaders = {
        'NZX': NZX_load_data
    }
    return data_loaders[market]


def NZX_load_data(market):
    raw_data = pd.read_csv("static/file_store/market_data/%s/cpi.csv" % market, header=[0, 1], skiprows=[2, 3, 4])

    values = raw_data['Consumers price index (CPI)', '(Index)']
    dates = pd.to_datetime(raw_data['Unnamed: 0_level_0', 'Unnamed: 0_level_1'])

    data = []
    for date, value in zip(dates, values):
        data.append({'measure': 'CPI', 'date': date, 'value': value})

    return data


def data_saver_csv(file, market, filename):
    if not os.path.exists("static/file_store/market_data/%s/" % (market,)):
        os.makedirs("static/file_store/market_data/%s/" % (market,))

    with open("static/file_store/market_data/%s/%s.csv" % (market, filename), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)