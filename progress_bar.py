from time import sleep
from tqdm import tqdm

def create_progress_bar(desc):
    ''' Create a progress bar with the iteration count and without the moving 
    '''
    return tqdm(desc = desc)


# def create_progress_bar(end, desc):
#     return tqdm(range(end), desc = desc)

def update_progress_bar(pbar,i):
    pbar.update(i)

def close_progress_bar(pbar):
    pbar.close()
