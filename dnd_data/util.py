import csv
import sys


def parse_csv(filename):
    """
    Takes a csv file filename, parses it and returns a list of dicts.
    :param filename:
    :return:
    """
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        data = []
        try:
            for row in reader:
                data.append(row)
            return data
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))