import csv

from pipeline.helpers import print_error, print_log
from pipeline.constants import *

def write_dataset(seq_map):
    ''' Writes all biomarker features into a csv to be used by ML models
    '''
    print_log("Writing biomarker features...")
    feature_keys = [
        "id",   # record id
        "circ_alignment_a", "circ_alignment_b", "circ_mismatches", "circ_count",    # circularity
        "a", "c", "g", "t", "gc", # gc content
        "inc_identity", "inc_length", "inc_bitscore", "inc_count",   # incompatibility factor
        "orit_identity", "orit_length", "orit_bitscore", "orit_count",   # orit
        "rrna_length", "rrna_bitscore", "rrna_count"    # rrna
        ]

    rows = []
    for key in seq_map.keys():
        row = [seq_map[key][x] for x in feature_keys[1:]]
        row.insert(0, key)
        rows.append(row)

    try:
        with open(dataset_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(feature_keys)
            writer.writerows(rows)
        print_log("Writing biomarker features completed\n")
            
    except IOError:
        print_error("I/O error while writing the biomarkers.")
