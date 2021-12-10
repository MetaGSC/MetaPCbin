import subprocess as sp
import os
import csv
from Bio import SeqIO

from pipeline.helpers import create_rrna_dirs, print_log, print_error
from pipeline.constants import *
from pipeline.progress_bar import *

def calc_rrna(cmscan_path, files, threads, seq_map):
    ''' Generates the rrna features for each sequence using cmscan
    '''
    print_log("Generating rrna features...")
    try:
        create_rrna_dirs()
        progress_bar = create_visual_progress_bar(len(seq_map), rrna_bar_desc)
        for filename in files:
            out_file = os.path.join(rrna_out_path, "temp.rrna.cmscan.tsv")
            db_file = os.path.join(db_path, 'rRNA')

            cmd = [
                cmscan_path,
                '--noali',
                '--cut_tc',
                '--cpu', str(threads),
                '--tblout', str(out_file),
                db_file,
                filename,
            ]

            proc = sp.run(
                cmd,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                universal_newlines=True
            )

            matches = {}
            if proc.returncode == 0:
                tsvfile = open(out_file)
                fh = csv.reader(tsvfile, delimiter="\t")
                for line in fh:
                    if(line[0][0] != '#'):
                        cols = line[0].strip().split()
                        id = cols[2]
                        length = abs(int(cols[8])- int(cols[7]))
                        bitscore = float(cols[14])

                        if id in matches.keys():
                            matches[id]['rRNA-length'] = \
                                (matches[id]['rRNA-length']*matches[id]['rRNA-count'] + length) \
                                    / (matches[id]['rRNA-count'] + 1)
                            matches[id]['rRNA-bitscore'] = \
                                (matches[id]['rRNA-bitscore']*matches[id]['rRNA-count'] + bitscore)\
                                    / (matches[id]['rRNA-count'] + 1)
                            matches[id]['rRNA-count'] += 1
                        else:
                            matches[id] = {
                                'rRNA-length': length,
                                'rRNA-bitscore': bitscore,
                                'rRNA-count': 1
                            }

            for record in SeqIO.parse(filename, 'fasta'):
                id = record.id
                if id in matches.keys():
                    seq_map[id].update(matches[id])

                else:
                    seq_map[id].update({'rRNA-length': 0, 'rRNA-bitscore': 0, 'rRNA-count': 0})
                update_progress_bar(progress_bar, 1)

        close_progress_bar(progress_bar)
        print_log("Generating rrna features completed.\n")

    except Exception as err:
        print_error(f"Error calculating rrna factor: {err}")
