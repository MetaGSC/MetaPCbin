import subprocess as sp
import os
from Bio import SeqIO

from pipeline.helpers import print_log, print_error
from pipeline.progress_bar import *
from pipeline.constants import *

def count_bases(seq):
    ''' Count and return the base % of a sequence
    '''
    sq_ln = len(seq)
    dir = {}
    dir['a'] = (seq.count("a") + seq.count("A"))/sq_ln
    dir['c'] = (seq.count("c") + seq.count("C"))/sq_ln
    dir['g'] = (seq.count("g") + seq.count("G"))/sq_ln
    dir['t'] = (seq.count("t") + seq.count("T"))/sq_ln
    dir['gc'] = dir["g"] + dir["c"]
    return dir


def gc_content(files, seq_map):
    ''' Generates the features related to the base percentages of sequences
    '''
    print_log("Generating gc content features...")
    try:
        progress_bar = create_visual_progress_bar(len(seq_map), gc_bar_desc)
        for file in files:
            for record in SeqIO.parse(file, 'fasta'):
                id = record.id
                perc = count_bases(record.seq)
                seq_map[id].update(perc)
                update_progress_bar(progress_bar, 1)
    
        close_progress_bar(progress_bar)
       
    except Exception as err:
        print_error(f"Error calculating gc content: {err}")
    
    print_log("Generating gc content features completed.\n")
