import csv


class StatisticsBase(object):
    def __init__(self, filename):
        self.days = {}
        fr = open(filename, 'r', encoding='utf-8')
        self.reader = csv.DictReader(fr)
