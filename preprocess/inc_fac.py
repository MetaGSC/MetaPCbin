import subprocess as sp
import os
from Bio import SeqIO

from helpers import create_inc_factor_dirs, print_error, print_log
from progress_bar import *
from constants import *

def calc_inc_factor(blastn_path, files, threads, seq_map):
    ''' Generates the incompatibility factor features for each sequence using blastn
    '''
    print_log("Generating incompatibility factor features...")
    try:
        create_inc_factor_dirs()
        progress_bar = create_visual_progress_bar(len(seq_map), inc_fac_desc)
        for filename in files:
            name = os.path.splitext(os.path.basename(filename))[0]
            out_file = os.path.join(incfac_out_path, "temp.inc.blast.out")
            db_file = os.path.join(db_path, "inc-types.fasta")

            cmd = [
                blastn_path,
                '-query', db_file,
                '-subject', filename,
                '-num_threads', str(threads),    
                '-perc_identity', '90',
                '-culling_limit', '1',
                '-outfmt', '6 qseqid sseqid pident length bitscore',
                '-out', out_file,
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
                        id = cols[1]
                        identity = float(cols[2])
                        length = int(cols[3])
                        bitscore = float(cols[4])

                        if id in matches.keys():
                            matches[id]['inc_identity'] = \
                                (matches[id]['inc_identity']*matches[id]['inc_count'] + identity) \
                                / (matches[id]['inc_count'] + 1)
                            matches[id]['inc_length'] = \
                                (matches[id]['inc_length']*matches[id]['inc_count'] + length) \
                                / (matches[id]['inc_count'] + 1)
                            matches[id]['inc_bitscore'] = \
                                (matches[id]['inc_bitscore']*matches[id]['inc_count'] + bitscore) \
                                / (matches[id]['inc_count'] + 1)
                            matches[id]['inc_count'] += 1
                        else:
                            matches[id] = {
                                'inc_identity': identity,
                                'inc_length': length,
                                'inc_bitscore': bitscore,
                                'inc_count': 1
                            }

            for record in SeqIO.parse(filename, 'fasta'):
                id = record.id
                if id in matches.keys():
                    seq_map[id].update(matches[id])
                else:
                    seq_map[id].update(
                        {'inc_identity':0, 'inc_length':0, 'inc_bitscore':0, 'inc_count':0 })
                update_progress_bar(progress_bar, 1)
    
        close_progress_bar(progress_bar)
        print_log("Generating incompatibility factor features completed.\n")
       
    except Exception as err:
        print_error(f"Error calculating inc. factor: {err}")
