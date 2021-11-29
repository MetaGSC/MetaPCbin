from random import randint
from Bio import SeqIO
import os

from pipeline.progress_bar import *
from pipeline.constants import *
from pipeline.helpers import create_fragment_dirs, print_error, print_log
    
def frag_generator(files, coverage):
    ''' Iterate through the input files and generate fragments
    '''
    frag_count = 0
    for filename in files:
        try:
            for record in SeqIO.parse(filename, 'fasta'):
                length = len(record.seq)
                fragments = []
                frag_count = min(frag_cnt_max, int(coverage*(length/frag_len))+1)
                for _ in range(frag_count):
                    if(length<frag_len):
                        rand_i = 0
                    else:
                        rand_i = randint(0, length-frag_len)
                    fragments.append(
                        {"n":frag_count, "id":record.id, 
                        "seq":str(record.seq)[rand_i:rand_i+min(frag_len, length)]}
                        )
                    frag_count+=1
                yield record.id, fragments

        except Exception as err:
            print_error(f"Error reading fasta file {filename}: {err}")

def write_frags(seq_id, seq_frags):
    ''' Write the generated fragments into files
    '''
    try:
        with open(os.path.join(frag_write_path, f'{seq_id}.fasta'), 'w+') as fout:
            for frag in seq_frags:
                fout.write(f'>{frag["n"]} {frag["id"]}\n{frag["seq"]}\n')
    except Exception as err:
       print_error(f"Error writing fragment fasta file: {err}")

def fragment(input_files, coverage):
    ''' Handler function for metagenomic fragment generation
    '''
    print_log("\nGenerating metagenomic fragments...")
    create_fragment_dirs()
    frag_count = {}

    frag_gen = frag_generator(input_files, coverage)

    progress_bar = create_progress_bar(frag_bar_desc)
    for input in enumerate(frag_gen):
        _, seqs = input
        seq_id, seq_frags = seqs
        seq_frag_count = len(seq_frags)
        write_frags(seq_id, seq_frags)
        update_progress_bar(progress_bar, seq_frag_count)
        frag_count[seq_id] = seq_frag_count

    close_progress_bar(progress_bar)
    print_log("Generating metagenomic fragments completed.\n")
    return frag_count
