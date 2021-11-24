import subprocess as sp
import os
from Bio import SeqIO

from pipeline.helpers import print_error, create_orit_dirs, print_log
from pipeline.constants import *
from pipeline.progress_bar import *

def calc_orit(blastn_path, files, threads, seq_map):
    ''' Generates the orit features for each sequence using blastn
    '''
    print_log("Generating orit features...")
    try:
        create_orit_dirs()
        progress_bar = create_visual_progress_bar(len(seq_map), orit_bar_desc)
        for filename in files:
            name = os.path.splitext(os.path.basename(filename))[0]
            out_file = os.path.join(orit_out_path, "temp.orit.blast.out")
            db_file = os.path.join(db_path, "orit")

            cmd = [
                blastn_path,
                '-query', str(filename),
                '-db', str(db_file),
                '-num_threads', str(threads),
                '-culling_limit', '1',
                '-perc_identity', '90',
                '-evalue', '1E-5',
                '-outfmt', '6 qseqid sseqid pident length bitscore',
                '-out', str(out_file)
            ]

            proc = sp.run(
                cmd,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                universal_newlines=True
            )
            
            matches = {}
            if proc.returncode == 0:
                with open(out_file, 'r') as fh:
                    for line in fh:
                        line = line.rstrip()
                        cols = line.split('\t')
                        id = cols[0]
                        identity = float(cols[2])
                        length = int(cols[3])
                        bitscore = float(cols[4])

                        if id in matches.keys():
                            matches[id]['OriT-identity'] = \
                                (matches[id]['OriT-identity']*matches[id]['OriT-count'] + identity)\
                                / (matches[id]['OriT-count'] + 1)
                            matches[id]['OriT-length'] = \
                                (matches[id]['OriT-length']*matches[id]['OriT-count'] + length) \
                                / (matches[id]['OriT-count'] + 1)
                            matches[id]['OriT-bitscore'] = \
                                (matches[id]['OriT-bitscore']*matches[id]['OriT-count'] + bitscore)\
                                / (matches[id]['OriT-count'] + 1)
                            matches[id]['OriT-count'] += 1
                        else:
                            matches[id] = {
                                'OriT-identity': identity,
                                'OriT-length': length,
                                'OriT-bitscore': bitscore,
                                'OriT-count': 1
                            }

            for record in SeqIO.parse(filename, 'fasta'):
                id = record.id
                if id in matches.keys():
                    seq_map[id].update(matches[id])
                else:
                    seq_map[id].update(
                        {'OriT-identity':0, 'OriT-length':0, 'OriT-bitscore':0, 'OriT-count':0 })
                update_progress_bar(progress_bar, 1)
    
        close_progress_bar(progress_bar)
        print_log("Generating orit features completed.\n")

    except Exception as err:
        print_error(f"Error calculating orit: {err}")
