import os
import json
import csv

# author: mattia rossi
# date: 04-07-2021
# objective: parse a json file, where each object is indexed by a millisecond (ms)
# timestamp (ts), and is written to a CSV file
# JSON input file: json_timhub.txt
# CSV output file: out.csv
# Liberally inspired by code at: https://github.com/jearlcalkins/scrape_dsl_modem_stats


# the application is hard coded, to recover all the variables in the list 'use'
# the initial list 'use' is complete, and one can remove variables, one at a time
# using the list.remove() method.  see the remove example below

# use the following data columns, and use in this order
use = ['SNR_downstream',
       'SNR_upstream',
       'Power_downstream',
       'Power_upstream',
       'dslDownstreamBitRate',
       'dslUpstreamBitRate',
       'dslMaxDownstreamBitRate',
       'dslMaxUpstreamBitRate',
       'dslDownstreamAttenuation',
       'dslUpstreamAttenuation',
       'dslLineStatusElement'
]

def build_header(columns):

    heading = list()
    heading.append("ts")
    
    for column in columns:
        heading.append(column)

    return heading
    
with open ("json_timhub.txt", "r") as fh, open("out.csv", "w", newline="") as fcsv:
    writer = csv.writer(fcsv)

    heading = build_header(use)
    writer.writerow(heading)
    
    for line in fh:        
        result = json.loads(line)
        ts = list(result)[0]
        samples = result[ts]
        
        row = list()
        row.append(ts)

        value_previous = -1
        for column_name in use:
            try:
                value = samples[column_name]
                row.append(value)
            except KeyError as Exception:
                row.append("NaN")
            
        writer.writerow(row)            
