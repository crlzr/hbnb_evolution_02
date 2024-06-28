#!/usr/bin/python3

import csv
from flask import send_file
import json

def export_to_file(data_to_print):
    """ exports data to file """
    # open a new CSV file for writing
    with open('output.csv', 'w', newline='') as csvfile:
        # creates the writer object to write to the file
        csvwriter = csv.writer(csvfile, delimiter = ',')
        header_row = []
        # iterates over the first dictionary to find header rows
        for k, v in data_to_print[0].items():
            header_row.append(k)
        # writes the header row to the CSV file
        csvwriter.writerow(header_row)
        # iterates over the list of dictionaries
        for row in data_to_print:
            data_list = []
            # iterates over the key-value pairs
            for k, v in row.items():
                data_list.append(v)
            # writes the value to the CSV file
            csvwriter.writerow(data_list)
    # returns / creates the CSV file
    return send_file('output.csv')

