from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from scipy.interpolate import make_interp_spline
import numpy as np
import pandas as pd
from numpy.random import randint
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

from pipeline.model.NNModule import Model
from pipeline.constants import *

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
    df = pd.read_csv(all_results_path+'/data.csv')
    features = list(df.columns)
    features.remove('id')
    features.sort()
    scaler = MinMaxScaler()
    scaler = pickle.load(open(scaler_path, 'rb'))
    df[features] = scaler.transform(df[features])
    return df, features


def read_kmer_file(seq_id):
    array = np.genfromtxt(all_results_path+"/kmers/"+seq_id, dtype=np.float64)
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
    kmer_arrays = read_kmer_file(sequence_id)
    # print(f'\nseq_id: {sequence_id} count: {len(kmer_arrays)}')
    total = 0
    tot_probs = torch.tensor([0.0, 0.0])
    for m in kmer_arrays:
        prediction, prob_tensor = get_prediction(torch.tensor(m), kmer_model)
        tot_probs += prob_tensor
        total += prediction
    # print(f'kmer_plasmid_avg: {total/len(kmer_arrays)} prob_total = {tot_probs}')
    probs_list = (tot_probs/(len(kmer_arrays))).tolist()
    probs_list.insert(0, len(kmer_arrays))
    probs_list.append(total/len(kmer_arrays))
    return probs_list


def predict_nn_rf(out_path):
    global kmer_model
    predictions = []
    biomer_model = setup_biomer_model(biomer_model_path)
    kmer_model = setup_kmer_model(kmer_model_path)
    sequence_df, features = get_sequence_data(biomer_scalar_path)

    seq_list = list(sequence_df['id'].unique())
    for seq in tqdm(seq_list):
        kmer_prediction = predict_kmer(seq)
        full_prediction = [seq]
        full_prediction.extend(kmer_prediction)
        # print(full_prediction)
        selected = sequence_df.loc[sequence_df['id'] == seq][features]
        full_prediction.extend(
            (biomer_model.predict_proba(selected))[0].tolist())
        full_prediction.append((biomer_model.predict(selected)).item())
        predictions.append(full_prediction)
        # print(
        #     f"biomer result: {biomer_model.predict(selected)} biomer result probs: {biomer_model.predict_proba(selected)}")
        # print(full_prediction)
    print('Writing NN, RF predictions...')
    predictions_df = pd.DataFrame(predictions, columns=['seq_id', 'fragment_count', 'kmer_chro_prob',
                                  'kmer_plas_prob', 'kmer_prediction_avg', 'biomer_chro_prob', 'biomer_plas_prob', 'biomer_prediction'])

    predictions_df['sum'] = (
        predictions_df['kmer_plas_prob'] + predictions_df['biomer_plas_prob'])/2
    predictions_df['product'] = (
        predictions_df['kmer_plas_prob'] * predictions_df['biomer_plas_prob'])**0.5
    predictions_df.to_csv(os.path.join(
        out_path, 'predictions.csv'), index=False)

    print('Plotting graphs...')

    sns.scatterplot(data=predictions_df,
                    x="kmer_plas_prob", y="biomer_plas_prob", alpha=0.4)

    xu = np.array([0.25, 0.35355, 0.5, 0.7071, 1])
    yu = np.array([1, 0.7071, 0.5, 0.35355, 0.25])
    X_Y_Spline = make_interp_spline(xu, yu)
    X_ = np.linspace(xu.min(), xu.max(), 500)
    Y_ = X_Y_Spline(X_)
    plt.plot(X_, Y_)

    xu = np.array([0, 0.2,  0.4,  0.6,  0.8,  1])
    yu = np.array([1, 0.8, 0.6, 0.4, 0.2, 0])
    X_Y_Spline = make_interp_spline(xu, yu)
    X_ = np.linspace(xu.min(), xu.max(), 500)
    Y_ = X_Y_Spline(X_)
    plt.plot(X_, Y_)
    
    plt.savefig(os.path.join(out_path, 'predictions_scatter.png'))
    plt.clf()
    sns.histplot(data=predictions_df, x="sum")
    plt.savefig(os.path.join(out_path, 'predictions_sum.png'))
    plt.clf()
    sns.histplot(data=predictions_df, x="product")
    plt.savefig(os.path.join(out_path, 'predictions_predict.png'))
    plt.clf()



if __name__ == "__main__":
    predict_nn_rf(all_results_path)
