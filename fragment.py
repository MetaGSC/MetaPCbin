from random import randint
from Bio import SeqIO

from progress_bar import *
from constants import *
from helpers import create_fragment_dirs, timestamp, print_error, print_log
    
def frag_generator(files, coverage):
    ''' Iterate through the input files and generate fragments
    '''
    frag_count = 0
    for filename in files:
        try:
            for record in SeqIO.parse(filename, 'fasta'):
                length = len(record.seq)
                fragments = []
                for _ in range(coverage):
                    if(length<frag_len):
                        rand_i = 0
                    else:
                        rand_i = randint(0, length-frag_len)
                    fragments.append(
                        {"n":frag_count, "id":record.id, 
                        "seq":str(record.seq)[rand_i:rand_i+min(frag_len, length)]}
                        )
                    frag_count+=1
                    if(length<frag_len):
                        break
                yield record.id, fragments

        except Exception as err:
            print_error(f"{timestamp()} Error reading fasta file {filename}: {err}\n")

def write_frags(seq_id, seq_frags):
    ''' Write the generated fragments into files
    '''
    try:
        with open(f'{frag_write_path}/{seq_id}.fasta', 'w+') as fout:
            for frag in seq_frags:
                fout.write(f'>{frag["n"]} {frag["id"]}\n{frag["seq"]}\n')
    except Exception as err:
       print_error(f"{timestamp()} Error writing fragment fasta file: {err}\n")

def fragment(input_files, coverage):
    ''' Handler function for metagenomic fragment generation
    '''
    print_log("Generating metagenomic fragments...")
    create_fragment_dirs()

    frag_gen = frag_generator(input_files, coverage)

    prog_bar = create_progress_bar(frag_bar_desc)
    for input in enumerate(frag_gen):
        _, seqs = input
        seq_id, seq_frags = seqs
        write_frags(seq_id, seq_frags)
        update_progress_bar(prog_bar, len(seq_frags))

    close_progress_bar(prog_bar)
    print_log("Generating metagenomic fragments completed.")
