from time import sleep
from tqdm import tqdm

def create_progress_bar(desc):
    ''' Create a progress bar with the iteration count
    '''
    return tqdm(desc = desc)


def create_visual_progress_bar(length, desc):
    ''' Create a progress bar with the moving needle
    '''
    return tqdm(range(length), desc = desc)

def update_progress_bar(pbar,i):
    pbar.update(i)

def close_progress_bar(pbar):
    pbar.close()
