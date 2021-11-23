from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from numpy.random import randint
import torch
import torch.nn as nn
from models.NNModule import Model
import pickle
from constants import *

kmer_model = None
biomer_model = None


def setup_kmer_model(model_path):
    model = Model(inputFeaturesSize, layer_array, outputSize)
    model.load_state_dict(torch.load(model_path))
    model.double()
    model.eval()
    return model


def setup_biomer_model(model_path):
    model = RandomForestClassifier(
        n_estimators=10, max_depth=10, random_state=1)
    model = pickle.load(open(model_path, 'rb'))
    return model


def get_sequence_data(scaler_path):
    df = pd.read_csv(predict_input_dir+'/data.csv')
    features = list(df.columns)
    features.remove('id')
    features.sort()
    scaler = MinMaxScaler()
    scaler = pickle.load(open(scaler_path, 'rb'))
    df[features] = scaler.transform(df[features])
    return df, features


def read_kmer_file(seq_id):
    array = np.genfromtxt(predict_input_dir+"/kmers/"+seq_id, dtype=np.float64)
    if(len(array.shape) == 1):
        temp = []
        temp.append(array)
        array = temp
    return array


def get_prediction(value, model):
    yb = model(value)
    # print(yb)
    _, preds = torch.max(yb, dim=0)
    # print(_.item(),preds.item())
    return preds.item(), yb


def predict_kmer(sequence_id):
    if(sequence_id == 'CP003983.1'):
        return
    kmer_arrays = read_kmer_file(sequence_id)
    print(f'\nseq_id: {sequence_id} count: {len(kmer_arrays)}')
    total = 0
    tot_probs = torch.tensor([0.0,0.0])
    for m in kmer_arrays:
        prediction, prob_tensor = get_prediction(torch.tensor(m), kmer_model)
        tot_probs += prob_tensor
        total += prediction
    print(f'kmer_plasmid_avg: {total/len(kmer_arrays)} prob_total = {tot_probs}')


if __name__ == "__main__":

    biomer_model = setup_biomer_model(biomer_model_path)
    kmer_model = setup_kmer_model(kmer_model_path)
    sequence_df, features = get_sequence_data(biomer_scalar_path)

    seq_list = list(sequence_df['id'].unique())
    for seq in seq_list:
        predict_kmer(seq)
        selected = sequence_df.loc[sequence_df['id'] == seq][features]
        print(
            f"biomer result: {biomer_model.predict(selected)} biomer result probs: {biomer_model.predict_proba(selected)}")
