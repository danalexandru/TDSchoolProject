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
def main(old_ver=None):
    """
    The function is the main section from which the project is being run

    :returns: Boolean (True or False)
    """
    try:
        if old_ver is True:
            # %% Use the Old Main Version
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
            # %% Else
        else:
            # %% Get the Matlab datasets
            dataset.get_all_matlab_csv_filenames('mean_freq')
            datasets = dataset.get_all_matlab_datasets()

            # %% Train the healthy dataset
            [dict_h_training_set, dict_h_valid_set, dict_h_test_set] = \
                dataset.split_dataset(datasets['healthy_data'][0])

            dict_h_training_set, dict_h_valid_set, dict_h_test_set = [
                dataset.clean_dataset(dict_h_training_set),
                dataset.clean_dataset(dict_h_valid_set),
                dataset.clean_dataset(dict_h_test_set)
            ]

            healthy_model = support_vector_classification.use_linear_kernel()
            dict_h_predicted_output = support_vector_classification.get_predicted_output(
                healthy_model,
                dict_h_training_set,
                dict_h_valid_set
            )

            dataset.plot_outputs(dict_h_valid_set['y'], dict_h_predicted_output['y_predicted'])

            # %% Train the broken  dataset
            [dict_b_training_set, dict_b_valid_set, dict_b_test_set] = \
                dataset.split_dataset(datasets['broken_data'][0])

            dict_b_training_set, dict_b_valid_set, dict_h_test_set = [
                dataset.clean_dataset(dict_b_training_set),
                dataset.clean_dataset(dict_b_valid_set),
                dataset.clean_dataset(dict_b_test_set)
            ]

            broken_model = support_vector_classification.use_linear_kernel()
            dict_b_predicted_output = support_vector_classification.get_predicted_output(
                broken_model,
                dict_b_training_set,
                dict_b_valid_set
            )

            dataset.plot_outputs(dict_b_valid_set['y'], dict_b_predicted_output['y_predicted'])
            
            # %% Exit
        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR)
        return False


if __name__ == '__main__':
    main()
