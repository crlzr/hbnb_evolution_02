#!/usr/bin/python3

import csv
from flask import send_file
import json

def export_to_file(data_to_print):
    """ exports data to file """
    # open a new CSV file for writing
    with open('test.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        header_row = []
        for k, v in data_to_print[0].items():
            header_row.append(k)
        csvwriter.writerow(header_row)

        for row in data_to_print:
            data_list = []
            for k, v in row.items():
                data_list.append(v)
            csvwriter.writerow(data_list)

    return send_file('test.csv',
                     mimetype='text/csv',
                     download_name='Output.csv',
                     as_attachment=True)
