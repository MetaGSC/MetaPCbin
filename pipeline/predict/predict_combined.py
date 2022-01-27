import pickle
from tqdm import tqdm
import os
import pandas as pd

from pipeline.constants import *

def setup_logistic_model(model_path):
    pipe = pickle.load(open(model_path, 'rb'))
    return pipe

def get_feature_data(out_path):
    df = pd.read_csv(os.path.join(out_path, 'predictions.csv'))
    features = ["kmer_plas_prob", "biomer_plas_prob"]
    return df, features

def get_sequence_lengths():
    len_df = pd.read_csv(os.path.join(seqlen_path))
    return len_df

def get_sequence_class(prob):
    if(prob<=CHROM_PRED_UPPER_BOUND):
        return 'chromosome'
    if(prob>=PLAS_PRED_LOWER_BOUND):
        return 'plasmid'
    return 'unclassified'

def predict_combined(out_path):
    predictions = []
    logistic_model = setup_logistic_model(logistic_model_path)
    data_df, features = get_feature_data(out_path)
    len_df = get_sequence_lengths()

    data_list = list(data_df['seq_id'].unique())
    for seq in tqdm(data_list):
        full_prediction = [seq]
        selected = data_df.loc[data_df['seq_id'] == seq][features]
        length = len_df.loc[len_df['seq_id'] == seq]['length'].values[0]
        
        proba = selected.iloc[0]['kmer_plas_prob']
        if(length>= KMER_MODEL_LEN_THRESHOLD):
            proba = logistic_model.predict_proba(selected)[0][1]
        seq_class = get_sequence_class(proba)
        full_prediction.append(proba)
        full_prediction.append(seq_class)
        predictions.append(full_prediction)

    predictions_df = pd.DataFrame(predictions, columns=['seq_id', 'plas_prob', 'class'])
    data_df['final_plas_prob'] = predictions_df['plas_prob']
    data_df['class'] = predictions_df['class']
    print('Writing combined predictions...')
    data_df.to_csv(os.path.join(out_path, 'predictions.csv'), index=False)
    
if __name__ == "__main__":
    predict_combined(all_results_path)
