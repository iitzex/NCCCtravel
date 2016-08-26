# -*- coding: utf-8 -*-
import csv
from travel import travel

if __name__ == '__main__':
    with open(u'參數設定.txt', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print row[0], row[1], row[2]
            travel(row[0], row[1].strip(), row[2])
