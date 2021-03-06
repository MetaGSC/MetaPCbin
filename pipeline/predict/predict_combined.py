import pickle
from tqdm import tqdm
import os
import pandas as pd
import sys

from pipeline.constants import *

def setup_logistic_model(model_path):
    pipe = pickle.load(open(model_path, 'rb'))
    return pipe

def get_sequence_lengths(out_path):
    len_df = pd.read_csv(os.path.join(out_path, 'seqlen.csv'))
    return len_df

def get_feature_data(out_path):
    feature_df = pd.read_csv(os.path.join(out_path, 'nn_rf_predictions.csv'))
    len_df = get_sequence_lengths(out_path)
    df = pd.merge(feature_df, len_df, on='seq_id', how="left")
    features = ["fragment_count", "kmer_plas_prob", "biomer_plas_prob", "length"]
    return df, features

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

    data_list = list(data_df['seq_id'].unique())
    for seq in tqdm(data_list):
        full_prediction = [seq]
        selected = data_df.loc[data_df['seq_id'] == seq][features]
        # length = len_df.loc[len_df['seq_id'] == seq]['length'].values[0]
        
        proba = logistic_model.predict_proba(selected)[0][1]
        seq_class = get_sequence_class(proba)
        full_prediction.append(proba)
        full_prediction.append(seq_class)
        predictions.append(full_prediction)

    predictions_df = pd.DataFrame(predictions, columns=['seq_id', 'plas_prob', 'class'])
    data_df['final_plas_prob'] = predictions_df['plas_prob']
    data_df['class'] = predictions_df['class']
    print('Writing combined predictions...')
    data_df.to_csv(os.path.join(out_path, 'final_predictions.csv'), index=False)
    
if __name__ == "__main__":
    out_path = sys.argv[1]
    predict_combined(out_path)
