import pandas as pd
import numpy as np
import os
from scipy import stats

data_dir = "Data Output/Experiment/"

# iterate over the files in the data directory
for fname in os.listdir(data_dir):
    # skip pesky mac hidden files
    if fname is not ".DS_Store": 
        # read in the data
        data = pd.read_csv(os.path.join(data_dir, fname)) 
        # log-transform GT-predict for plotting on logarithmic scale and exponential slope estimation
        data['GT_predict_log'] = np.log10(data['GT_predict'])

        """
        Run main evaluation script here for each data file
        """
        evaluation = []
        for dataset, dataset_data in data.groupby("dataset"):
            for method, method_data in dataset_data.groupby("method"):
                print method_data.columns
                # correlation with the TRUE
                corr_true = stats.linregress(method_data['GT_predict'], method_data['new_TRUE'])[2]
                # slope
                decline_slope = stats.linregress(method_data['timeSlice'], method_data['GT_predict'])[0]
                # exponent slope
                exponent_slope = stats.linregress(method_data['timeSlice'], method_data['GT_predict_log'])[0]
                # add to evaluation data
                evaluation.append({'dataset': dataset, 
                                   'method': method.split("_")[0], 
                                   'threshold': method.split("_")[1], 
                                   'run': method,
                                   'corr_true': corr_true,
                                   'decline_slope': decline_slope,
                                   'exp_slope': exponent_slope})
        # convert to pandas data frame
        evaluation = pd.DataFrame(evaluation)
        # output to file
        outname = "Data Output/evaluate_%s" %fname
        evaluation.to_csv(outname)
