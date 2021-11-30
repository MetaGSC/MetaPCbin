kmer_model_path = 'models/kmerModule100K.pth'
biomer_model_path = 'models/biomer_model.sav'
biomer_scalar_path = 'models/biomer_minmax_scaler.sav'
predict_input_dir = '/home/gayal/code/pipeline/results-plsdb-1000'

k=7
inputFeaturesSize = int((4**k) / 2)
layer_array = [512, 256]
outputSize = 2
