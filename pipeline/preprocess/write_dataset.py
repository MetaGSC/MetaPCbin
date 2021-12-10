import csv

from pipeline.helpers import print_error, print_log
from pipeline.constants import *

def write_dataset(seq_map):
    ''' Writes all biomarker features into a csv to be used by ML models
    '''
    print_log("Writing biomarker features...")
    feature_keys = [
        "id",   # record id
        "Cir-alignment_a_mean", "Cir-alignment_b_mean", "Cir-mismatches_mean", "Cir-count",    # circularity
        "a%", "c%", "g%", "t%", "gc-content", # gc content
        "IF-identity", "IF-length", "IF-bitscore", "IF-count",   # incompatibility factor
        "OriT-identity", "OriT-length", "OriT-bitscore", "OriT-count",   # orit
        "rRNA-length", "rRNA-bitscore", "rRNA-count"    # rrna
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
