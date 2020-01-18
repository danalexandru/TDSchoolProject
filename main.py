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
            dataset.trim_matlab_filenames(1)
            datasets = dataset.get_all_matlab_datasets()
            combined_dataset = dataset.combine_datasets(datasets)
            
            # %% Split into training, valid and test sets
            [dict_training_set, dict_valid_set, dict_test_set] = dataset.split_dataset(combined_dataset)
            [dict_training_set, dict_valid_set, dict_test_set] = [
                dataset.clean_dataset(dict_training_set),
                dataset.clean_dataset(dict_valid_set),
                dataset.clean_dataset(dict_test_set)
            ]
            
            # %% Use linear kernel SVM
            model = support_vector_classification.use_linear_kernel()
            
            # %% Use polynomial kernel SVM
            model = support_vector_classification.use_polynomial_kernel()
 
            # %% Use radial basis function kernel SVM
            model = support_vector_classification.use_radial_basis_function_kernel()
            
            # %% Train the SVM and predict the output
            dict_predic_valid = support_vector_classification.get_predicted_output(model, dict_training_set, dict_valid_set)
            dataset.plot_outputs(dict_valid_set['y'], dict_predic_valid['y_predicted'], 1)
            
            dict_predict_test = support_vector_classification.get_predicted_output(model, dict_training_set, dict_test_set)
            dataset.plot_outputs(dict_test_set['y'], dict_predict_test['y_predicted'], 2)
            
            # %% Get classification report
            classification_report = support_vector_classification.get_classification_report(dict_valid_set['y'], dict_predic_valid['y_predicted'])
            console.log('\n' + classification_report, console.LOG_INFO)
            
            classification_report = support_vector_classification.get_classification_report(dict_test_set['y'], dict_predict_test['y_predicted'])
            console.log('\n' + classification_report, console.LOG_INFO)
            
            # %% Get confusion matrix
            confusion_matrix = support_vector_classification.get_confusion_matrix(dict_valid_set['y'], dict_predic_valid['y_predicted'])
            console.log('\n' + str(confusion_matrix), console.LOG_INFO)
            
            confusion_matrix = support_vector_classification.get_confusion_matrix(dict_test_set['y'], dict_predict_test['y_predicted'])
            console.log('\n' + str(confusion_matrix), console.LOG_INFO)
            
            # %% Exit
        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR)
        return False


if __name__ == '__main__':
    main()
