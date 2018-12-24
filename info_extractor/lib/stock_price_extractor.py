import pandas as pd
import numpy as np
import os


def csv_exists(filename, company):
    return os.path.isfile("static/file_store/csv/%s/%s.csv" % (company, filename))


def extract_csv(filename, company) -> pd.DataFrame:
    """
    Expects the csv file to have the columns Data, Open, High, Low, Close, Adj Close and Volume
    :param filename:
    :param company:
    :return:
    """
    data = pd.read_csv("static/file_store/csv/%s/%s.csv" % (company, filename))

    return data


def save_csv_file(csv_file, filename, company):
    """
    Saves a csv file to disk
    Todo use the dates to combine exiting data with the new data
    :param csv_file:
    :param filename:
    :param company:
    :return:
    """
    if not os.path.exists("static/file_store/csv/%s/" % (company,)):
        os.makedirs("static/file_store/csv/%s/" % (company,))

    with open("static/file_store/csv/%s/%s.csv" % (company, filename), 'wb+') as destination:
        for chunk in csv_file.chunks():
            destination.write(chunk)