from pipeline.predict.predict_nn_rf import predict_nn_rf
from pipeline.predict.predict_combined import predict_combined
from pipeline.constants import *

def predict(out_path):
    predict_nn_rf(out_path)
    predict_combined(out_path)
    
if __name__ == "__main__":
    predict(all_results_path)
