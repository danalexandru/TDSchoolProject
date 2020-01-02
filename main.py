# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:09:17 2019

@author: Dan Alexandru-Bogdan
"""
# %% Imports
from globals import console
#from get_csv_files import get_csv_files
from dataset import dataset, support_vector_classification


# %% Main
def main():
    """
    The function is the main section from which the project is being run

    :returns: Boolean (True or False)
    """
    try:
        dataset.get_all_csv_filenames()
        dataset.trim_filenames(1)
        datasets = dataset.get_all_datasets()
        
        combined_dataset = dataset.combine_datasets(datasets)
        [dict_training_set, dict_valid_set, dict_test_set] = dataset.split_dataset(combined_dataset)
        dict_training_set, dict_valid_set, dict_test_set = [
                dataset.clean_dataset(dict_training_set),
                dataset.clean_dataset(dict_valid_set),
                dataset.clean_dataset(dict_test_set)
                ]
        
        model = support_vector_classification.use_linear_kernel()
        dict_predicted_output = support_vector_classification.get_predicted_output(
                model,
                dict_training_set,
                dict_valid_set
                )
        
        dataset.plot_outputs(dict_valid_set['y'], dict_predicted_output['y_predicted'])
        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR)
        return False


if __name__ == '__main__':
    main()
