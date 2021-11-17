import subprocess as sp
import concurrent.futures
from Bio import SeqIO
import os

from progress_bar import *
from helpers import print_error, print_log
from constants import *
from helpers import create_circ_dirs, find_mean, delete_dir_if_exist

def circ_helper(nucmer_path, record):
    ''' Generates the circularity features for single metagenomic record using nucmer
    '''
    record_map = {}
    id = record.id
    try:
        # break the string into 2 parts and compare
        seq_mid = int(len(record.seq)/2)
        seq_a = str(record.seq[:seq_mid])
        seq_b = str(record.seq[seq_mid:])

        seq_a_file = os.path.join(circ_split_path, f'{id}_a.fasta')
        seq_b_file = os.path.join(circ_split_path, f'{id}_b.fasta')
        with open(seq_a_file, mode='w+') as fout:
            fout.write(f'>{id}_a\n')
            fout.write(seq_a + '\n')
        
        with open(seq_b_file, mode='w+') as fout:
            fout.write(f'>{id}_b\n')
            fout.write(seq_b + '\n')

        out_file = os.path.join(circ_out_path, f"{id}_temp")
        
        cmd = [
        nucmer_path,
        '-f',  # only forward strand
        '-l', '40',  # increase min match length to 40 bp
        '-p', out_file,
        seq_a_file,
        seq_b_file
        ]
        proc = sp.run(
            cmd,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            universal_newlines=True,
        )
        alignment_a_sum, alignment_b_sum, mismatches_sum, count = 0, 0, 0, 0
        if(proc.returncode == 0):
            has_match = False
            with open(f"{out_file}.delta") as fout:
                for line in fout:
                    line = line.rstrip()
                    if(line[0] == '>'):
                        has_match = True
                    elif(has_match):
                        cols = line.split(' ')
                        if(len(cols) == 7):
                            start_b = int(cols[0])
                            end_b = int(cols[1])
                            start_a = int(cols[2])
                            end_a = int(cols[3])
                            mismatches = int(cols[4])
                            alignment_a = end_a - start_a + 1
                            alignment_b = end_b - start_b + 1
                            mismatches_sum += mismatches
                            alignment_a_sum += alignment_a
                            alignment_b_sum += alignment_b
                            count+=1
        
        alignment_a_mean = find_mean(alignment_a_sum, count)
        alignment_b_mean = find_mean(alignment_b_sum, count)
        mismatches_mean = find_mean(mismatches_sum, count)

        record_map['circ_alignment_a'] = alignment_a_mean
        record_map['circ_alignment_b'] = alignment_b_mean
        record_map['circ_mismatches'] = mismatches_mean
        record_map['circ_count'] = count

        delete_dir_if_exist(seq_a_file)
        delete_dir_if_exist(seq_b_file)
        delete_dir_if_exist(f"{out_file}.delta")
        delete_dir_if_exist(f"{out_file}.ntref")
        delete_dir_if_exist(f"{out_file}.mgaps")

    except Exception as err:
        print_error(f"Error computing circularity for record {record}: {err}")

    return id, record_map

def circ_directory_worker(nucmer_path, filename):
    ''' worker for input in directory format with large number of files 
    '''
    sub_seq_map = {}
    record_count = 0
    try:
        for record in SeqIO.parse(filename, 'fasta'):
            record_count+=1
            id, record_map = circ_helper(nucmer_path, record)
            sub_seq_map[id] = record_map
    except Exception as err:
        print_error(f"Error reading file {filename}: {err}")
    return record_count, sub_seq_map

def circ_file_worker(nucmer_path, filename, rid):
    ''' worker for input in file format with one or few files with large number of records in each
    '''
    this_rec = None
    record_map = None
    try:
        for record in SeqIO.parse(filename, 'fasta'):
            if(rid == record.id):
                this_rec = record
                break
        id, record_map = circ_helper(nucmer_path, this_rec)
        
    except Exception as err:
        print_error(f"Error reading file {filename}: {err}")
    return rid, record_map

def merge_maps(seq_map, sub_maps):
    ''' Merges the sequence map with the result maps from different threads
    '''
    for map in sub_maps:
        for k, v in map.items():
            seq_map[k].update(v)

def calc_circularity(nucmer_path, threads, files, seq_map, input_mode):
    ''' Generates the circularity features for each sequence using nucmer
    '''
    print_log("Generating circularity features...")

    create_circ_dirs()
    progress_bar = create_visual_progress_bar(len(seq_map), circ_bar_desc)
    executor = concurrent.futures.ProcessPoolExecutor(threads)

    if(input_mode == DIRECTORY_INPUT):
        # -d type input
        # Assumes a directory of larger number of file
        # with smaller number of records in each file
        futures = [
            executor.submit(
                circ_directory_worker, nucmer_path, filename)
                for filename in files
            ]
        sub_maps = []
        for f in concurrent.futures.as_completed(futures):
            record_count, sub_map = f.result()
            update_progress_bar(progress_bar, record_count)
            sub_maps.append(sub_map)
        executor.shutdown(wait=True)
        merge_maps(seq_map, sub_maps)


    elif(input_mode == FILE_INPUT):
        # -r type input
        # Assumes one or few files of input
        # with larger number of records in each file
        for filename in files:
            try:
                records = []
                for record in SeqIO.parse(filename, 'fasta'):
                    records.append(record.id)
                futures = [
                    executor.submit(
                        circ_file_worker, nucmer_path, filename, rid)
                        for rid in records
                    ]
                for f in concurrent.futures.as_completed(futures):
                    id, record_map = f.result()
                    seq_map[id].update(record_map)
                    update_progress_bar(progress_bar, 1) 
                executor.shutdown(wait=True)

            except Exception as err:
                print_error(f"Error reading file {filename}: {err}")

    close_progress_bar(progress_bar)
    print_log("Generating circularity features completed.")
