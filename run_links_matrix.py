# Jeff Starr, 4 October, 2017

# This is a program that calls the links_matrix function then 
# writes the data returned into two files.

# os module: https://docs.python.org/3.6/library/os.html

import csv
import json
import os
from links_matrix_function import process_links_matrix

links_input_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Custom_Links_Flattener_data/input_matrix_20171002.csv"
    )

links_output_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Custom_Links_Flattener_data/output_records_20171002.csv"
    )

history_input_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Custom_Links_Flattener_data/links_history24092017.csv"
    )

history_output_filename = os.path.expanduser(
    "~/Documents/Coding/Projects/" +
    "PRODUCTION_DATA/Custom_Links_Flattener_data/links_history20171002.csv"
    )

(output_matrix, history_matrix) = process_links_matrix(
    links_input_filename,
    history_input_filename)

with open(links_output_filename, 'w', encoding='utf-8') as f_write:
    writer = csv.writer(f_write)
    for row in output_matrix:
        writer.writerow(row)

with open(history_output_filename, 'w', encoding='utf-8') as f_write:
    writer = csv.writer(f_write)
    for row in history_matrix:
        writer.writerow(row)