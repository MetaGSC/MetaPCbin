import subprocess as sp
import os
from Bio import SeqIO

from pipeline.helpers import create_inc_factor_dirs, print_error, print_log
from pipeline.progress_bar import *
from pipeline.constants import *

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
                            matches[id]['IF-identity'] = \
                                (matches[id]['IF-identity']*matches[id]['IF-count'] + identity) \
                                / (matches[id]['IF-count'] + 1)
                            matches[id]['IF-length'] = \
                                (matches[id]['IF-length']*matches[id]['IF-count'] + length) \
                                / (matches[id]['IF-count'] + 1)
                            matches[id]['IF-bitscore'] = \
                                (matches[id]['IF-bitscore']*matches[id]['IF-count'] + bitscore) \
                                / (matches[id]['IF-count'] + 1)
                            matches[id]['IF-count'] += 1
                        else:
                            matches[id] = {
                                'IF-identity': identity,
                                'IF-length': length,
                                'IF-bitscore': bitscore,
                                'IF-count': 1
                            }

            for record in SeqIO.parse(filename, 'fasta'):
                id = record.id
                if id in matches.keys():
                    seq_map[id].update(matches[id])
                else:
                    seq_map[id].update(
                        {'IF-identity':0, 'IF-length':0, 'IF-bitscore':0, 'IF-count':0 })
                update_progress_bar(progress_bar, 1)
    
        close_progress_bar(progress_bar)
        print_log("Generating incompatibility factor features completed.\n")
       
    except Exception as err:
        print_error(f"Error calculating inc. factor: {err}")
