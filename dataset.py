# %% Imports
from globals import console
from tkinter.filedialog import askopenfilename
from random import randrange
from numbers import Number
import glob
import os
import ntpath

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.preprocessing import Imputer

import pandas as pd
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# %% class Dataset
class Dataset(object):
    """
    This class deals with the datasets 
    """
    def __init__(self):
        self.csvs_folder = {
        'main': 'csvs',
        'healthy_data': 'csvs/Healthy Data',
        'broken_data': 'csvs/BrokenTooth Data'
        }
        self.csv_filenames = {}
        
        self.matlab_results_folder = {
                'main': 'csvs/Matlab Results',
                'healthy_data': 'csvs/Matlab Results/Healthy Data',
                'broken_data': 'csvs/Matlab Results/BrokenTooth Data'}
        self.matlab_results_filenames = {}
        self.matlab_results_keywords = [
                'mean_freq',
                'freq_magn',
                'kustosis',
                'skewness',
                'entropy',
                'iqr'
                ]
        
    def get_dataset(self, path=None):
        """
        This method returns the dataset of a csv file
        
        :param path: (String) The path of the csv file
        :return: (Dictionary) A Dictionary containing the dataset, and the features of that csv file
            {
                'name': <String>,
                'X': <Numpy Array>,
                'y': <Numpy Array>,
                'Ts': <Integer>,
                'frequency': <Integer>
            }
        """
        try:
            # Ask user for file path if not mentioned
            if path is None:
                path = askopenfilename(initialdir=str(os.path.dirname(os.path.abspath(__file__)) + '/csvs'),
                                             filetypes=[("Csv files", "*.csv")])
                
            filename = str(ntpath.basename(path)).replace('.csv', '')
            
            # Get feature values
            X = pd.read_csv(path).iloc[:, :].values
            
            # Get target value
            if 'healthy' in str(path).lower():
                y = np.zeros((X.shape[0], 1))
            elif 'broken' in str(path).lower():
                y = np.ones((X.shape[0], 1))
            else:
                console.log('Could not determine whether %s is \'healthy\' or \'broken\'.' % filename,
                            console.LOG_WARNING)
                return False
                
            return {
                    'name': filename,
                    'X': X,
                    'y': y,
#                    'Ts': int(filename[5:]),
                    'Ts': int(filename[1:3]),
                    'frequency': int(filename[1:3])
                    }
            
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def get_all_csv_filenames(self):
        """
        This method returns the names of all the files from the 2 project directories
        
        :return: (Dictionary) A dictionary containing 2 Lists (each with the filenames from their respective directory)
            {
                'healthy_data': <List<String>>,
                'broken_data': <List<String>>
            }
        """
        try:
            healthy_data_filenames = glob.glob(self.csvs_folder['healthy_data'] + '/*.csv')
            broken_data_filenames = glob.glob(self.csvs_folder['broken_data'] + '/*.csv')
            
            self.csv_filenames = {
                    'healthy_data': healthy_data_filenames,
                    'broken_data': broken_data_filenames
                    }
            
            return self.csv_filenames
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def trim_filenames(self, number=None):
        """
        This method trims the filenames from the 'self.csv_filenames' parameter to reduce complexity
        
        :param number: (Integer) The number of filenames you want per folder (Default: All of them)
        :return: (Dictionary) A dictionary containing 2 Lists (each with a subset of filenames from their respective directory)
            {
                'healthy_data': <List<String>>,
                'broken_data': <List<String>>
            }
        """
        try:
            if number is None:
                return self.csv_filenames
            elif not isinstance(number, int) or number <= 0:
                console.log('Invalid \'number\' value %s. It should be a positive Integer.' % str(number),
                            console.LOG_WARNING)
                return False
            
            # Get the number of files in a folder
            N = len(self.csv_filenames['healthy_data'])
            
            csv_filenames = {
                    'healthy_data': [],
                    'broken_data': []
                    }

            i = 0
            while i < number:
                index = randrange(N)
                
                if self.csv_filenames['healthy_data'][index] in csv_filenames['healthy_data'] or \
                    self.csv_filenames['broken_data'][index] in csv_filenames['broken_data']:
                        continue
                    
                csv_filenames['healthy_data'].append(self.csv_filenames['healthy_data'][index])
                csv_filenames['broken_data'].append(self.csv_filenames['broken_data'][index])
                i += 1
                
            self.csv_filenames = csv_filenames
            return self.csv_filenames
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def get_all_datasets(self):
        """
        This method returns all the datasets from the 'self.csv_filenames' files
        
        :return: (Dictionary) A dictionary containing the features and targets for all the files selected
                {
                    'healthy_data': [
                    {
                        'name': <String>,
                        'X': <Numpy Array>,
                        'y': <Numpy Array>,
                        'Ts': <Integer>,
                        'frequency': <Integer>
                    }],
                    'broken_data': [
                    {
                        'name': <String>,
                        'X': <Numpy Array>,
                        'y': <Numpy Array>,
                        'Ts': <Integer>,
                        'frequency': <Integer>
                    }]
                    
                }
        """
        try:
            datasets = {
                    'healthy_data': [],
                    'broken_data': []
                    }
            # Get the Healthy Datasets
            for path in self.csv_filenames['healthy_data']:
                datasets['healthy_data'].append(self.get_dataset(path))
                
            # Get the Broken Datasets
            for path in self.csv_filenames['broken_data']:
                datasets['broken_data'].append(self.get_dataset(path))

            return datasets
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def combine_datasets(self, datasets):
        """
        This method combines all the datasets from the 2 types of data into one dataset
        
        :param datasets: (Dictionary) The result returned by the 'self.get_all_datasets' method
        :returns: (Dictionary) A single dictionary containing all the features and targets in one place
        """
        try:
            X = np.array(())
            y = np.array(())
            
            # Append the Healthy datasets
            for dataset in datasets['healthy_data']:
                if X.shape[0] == 0 or y.shape[0] == 0:
                    X = dataset['X']
                    y = dataset['y']
                else:
                    X = np.concatenate((X, dataset['X']))
                    y = np.concatenate((y, dataset['y']))
                
            # Append the Broken datasets
            for dataset in datasets['broken_data']:
                if X.shape[0] == 0 or y.shape[0] == 0:
                    X = dataset['X']
                    y = dataset['y']
                else:
                    X = np.concatenate((X, dataset['X']))
                    y = np.concatenate((y, dataset['y']))
                    
            return {
                    'X': X,
                    'y': y
                    }
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def split_dataset(self, dataset, test_size=0.2):
        """
        This method splits the dataset into training, valid and test set
        
        :param dataset: (Dictionary) A dictionary containing the features and targets of the current dataset
            {
                'X': <Numpy Array>,
                'y': <Numpy Array>
            }
        :param test_size: The percentage of the test and valid sets
        :return: (Dictionaries) 3 Dictionaries containing the features and targets for the training, valid and test sets
            of type 
            {
                'X': <Numpy Array>,
                'y': <Numpy Array>
            }
        """
        try:
            if not isinstance(test_size, Number) or \
                    test_size < 0 or \
                    test_size > 1:
                console.log('Invalid \"test_size\" value. It should be a number between (0, 1)', console.LOG_WARNING)
                return False
            
            # Initialize the training, valid and test sets dictionaries
            dict_training_set = {
                    'X': None,
                    'y': None
                    }
            
            dict_valid_set = {
                    'X': None,
                    'y': None
                    }
            
            dict_test_set = {
                    'X': None,
                    'y': None
                    }
            
            # Intermediary step (Get the test set)
            (
                dict_training_set['X'],
                dict_test_set['X'],
                dict_training_set['y'],
                dict_test_set['y']
            ) = train_test_split(
                dataset['X'],
                dataset['y'],
                test_size=test_size,
                random_state=0
            )
            
            # Final step (Get the trainign and valid set)
            (
                dict_training_set['X'],
                dict_valid_set['X'],
                dict_training_set['y'],
                dict_valid_set['y']
            ) = train_test_split(
                dict_training_set['X'],
                dict_training_set['y'],
                test_size=test_size,
                random_state=0
            )
            
            return dict_training_set, dict_valid_set, dict_test_set
        
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
        
    def save_split_dataset_as_mat(self, dict_training_set, dict_valid_set, dict_test_set):
        """
        This method saves the 'dict_training_set', 'dict_valid_set', and 'dict_test_set' JSONs returned by the 
            'split_dataset' method as a .mat file in order to be used in matlab
        """
        try:
            sio.savemat('training_set.mat', dict_training_set)
            sio.savemat('valid_set.mat', dict_valid_set)
            sio.savemat('test_set.mat', dict_test_set)
            
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
        
    def save_all_datasets_as_mat(self, dict_datasets):
        """
        This method saves the datasets recovered from the csv gearbox csv files into mats. Note that this method is 
            different from the 'save_split_dataset_as_mat' method, since it doesn't save the training, valid and test
            sets, but takes all the datasets (uncombined) and saves them basen on their names
            
        :param dict_datasets: (Dictionary) A dictionary containing the features and targets for all the files selected
        {
            'healthy_data': [
            {
                'name': <String>,
                'X': <Numpy Array>,
                'y': <Numpy Array>,
                'Ts': <Integer>,
                'frequency': <Integer>
            }],
            'broken_data': [
            {
                'name': <String>,
                'X': <Numpy Array>,
                'y': <Numpy Array>,
                'Ts': <Integer>,
                'frequency': <Integer>
            }]
            
        }
        :return: Boolean (True or False)            
        """
        try:
            sio.savemat('datasets.mat', dict_datasets)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def clean_dataset(self, dict_dataset):
        """
        This method cleans a dataset of it's NaN values
        
        :param dict_dataset: (Dictionary) A dataset containing targets and values
            {
                'X': <Numpy Array>,
                'y': <Numpy Array>
            }
        :return: (Dictionary) The cleaned dataset
        """
        try:
            # Retrieve targets and values from the dictionary
            X = dict_dataset['X']
            y = dict_dataset['y']
            
            # Create simple imputer
            imputer = Imputer(missing_values = np.nan, 
                              strategy = "mean")
            
            # Clean the features
            imputer.fit(X)
            X = imputer.transform(X)
            
            # Clean the targets
            imputer.fit(y)
            y = imputer.transform(y)
            
            return {
                    'X': X,
                    'y': y
                    }
            
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
        
    def plot_outputs(self, y_real, y_predicted, index=1):
        """
        This method plots the real targets and the predicted targets
        
        :param y_real: (Numpy Array) A column vector containing the real validation target values
        :param y_predicted: (Numpy Array) A column vector containing the predicted validation target values
        :return: Boolean (True or False)
        """
        try:
            plt.figure(index)
            plt.scatter(x=np.arange(y_real.size),
                        y=y_real,
                        color='red',
                        label='Real target values')
            plt.scatter(x=np.arange(y_predicted.size),
                        y=y_predicted,
                        color='blue',
                        label='Predicted target values')
            
            plt.grid(color='silver',
                     linestyle='--',
                     linewidth=1)
            
            plt.legend(loc='best')
            
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def get_all_matlab_csv_filenames(self, method):
        """
        This method returns all the .mat dictionaries filenames saved in the self.matlab_results_folder
        
        :param method: (String) The method that was used in matlab (Must be one of the self.matlab_results_keywords)
        :return: (List) A list containing all the .mat filenames of the matlab results saved in the 
            self.matlab_results_folder
        """
        try:
            if method not in self.matlab_results_keywords:
                console.log('Unrecognized method \'%s\'. It should be one of these methods: \n%s.' % 
                            (
                                    str(method),
                                    str(self.matlab_results_keywords)
                                    ), 
                            console.LOG_WARNING
                            )
                return False
                    
            healthy_data_filenames = glob.glob(self.matlab_results_folder['healthy_data'] + '/' + method + '/*.csv')
            broken_data_filenames = glob.glob(self.matlab_results_folder['broken_data'] + '/' + method + '/*.csv')
            
            self.matlab_results_filenames = {
                    'healthy_data': healthy_data_filenames,
                    'broken_data' : broken_data_filenames}
            
            return self.matlab_results_filenames
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def get_all_matlab_datasets(self):
        """
        This method returns all the datasets calculated and saved in matlab using a specific method. The method was 
            already specified in the 'self.get_all_matlab_csv_filenames' method. It must be one of the 
            self.matlab_results_keywords.
            
        :return: (Dictionary) A dictionary containing the features and targets for all the files selected
                {
                    'healthy_data': [
                    {
                        'name': <String>,
                        'X': <Numpy Array>,
                        'y': <Numpy Array>,
                        'Ts': <Integer>,
                        'frequency': <Integer>
                    }],
                    'broken_data': [
                    {
                        'name': <String>,
                        'X': <Numpy Array>,
                        'y': <Numpy Array>,
                        'Ts': <Integer>,
                        'frequency': <Integer>
                    }]
                    
                }
        """
        try:
            datasets = {
                    'healthy_data': [],
                    'broken_data': []
                    }
            
            # Get the Healthy Datasets
            for path in self.matlab_results_filenames['healthy_data']:
                datasets['healthy_data'].append(self.get_dataset(path))
                
            # Get the Broken Datasets
            for path in self.matlab_results_filenames['broken_data']:
                datasets['broken_data'].append(self.get_dataset(path))
                
            return datasets
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def trim_matlab_filenames(self, number=None):
        """
        This method trims the filenames from the 'self.matlab_results_filenames' parameter to reduce complexity
        
        :param number: (Integer) The number of filenames you want per folder (Default: All of them)
        :return: (Dictionary) A dictionary containing 2 Lists (each with a subset of filenames from their respective directory)
            {
                'healthy_data': <List<String>>,
                'broken_data': <List<String>>
            }
        """
        try:         
            if number is None:
                return self.matlab_results_filenames
            elif not isinstance(number, int) or number <= 0:
                console.log('Invalid \'number\' value %s. It should be a positive Integer.' % str(number),
                            console.LOG_WARNING)
                return False
            
            # Get the number of files in a folder
            N = len(self.matlab_results_filenames['healthy_data'])
            
            csv_filenames = {
                    'healthy_data': [],
                    'broken_data': []
                    }
    
            i = 0
            while i < number:
                index = randrange(N)
                
                if self.matlab_results_filenames['healthy_data'][index] in csv_filenames['healthy_data'] or \
                    self.matlab_results_filenames['broken_data'][index] in csv_filenames['broken_data']:
                        continue
                    
                csv_filenames['healthy_data'].append(self.matlab_results_filenames['healthy_data'][index])
                csv_filenames['broken_data'].append(self.matlab_results_filenames['broken_data'][index])
                i += 1
                
            self.matlab_results_filenames = csv_filenames
            return self.csv_filenames
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def save_all_datasets_as_split_datasets_mat(self, dict_datasets):
        """
        This method saves all the datasets retrieved as a mat file with the training, valid, test split already made
        
        :param dict_datasets: (Dictionary) A dictionary containing the features and targets for all the files selected
                {
                    'healthy_data': [
                    {
                        'name': <String>,
                        'X': <Numpy Array>,
                        'y': <Numpy Array>,
                        'Ts': <Integer>,
                        'frequency': <Integer>
                    }],
                    'broken_data': [
                    {
                        'name': <String>,
                        'X': <Numpy Array>,
                        'y': <Numpy Array>,
                        'Ts': <Integer>,
                        'frequency': <Integer>
                    }]
                    
                }
        :return: Boolean (True of False)
        """
        try:
            healthy_data = []
            broken_data = []
            
            # Get all the training, valid and test splits for the healthy datasets
            for data in dict_datasets['healthy_data']:
                [dict_training_set, dict_valid_set, dict_test_set] = self.split_dataset(data)
                [dict_training_set, dict_valid_set, dict_test_set] = [
                    self.clean_dataset(dict_training_set),
                    self.clean_dataset(dict_valid_set),
                    self.clean_dataset(dict_test_set)
                ]
                
                healthy_data.append({
                        'name': data['name'],
                        'Ts': data['Ts'],
                        'frequency': data['frequency'],
                        'training': dict_training_set,
                        'valid': dict_valid_set,
                        'test': dict_test_set
                    })
            
            # Get all the training, valid and test splits for the broken datasets
            for data in dict_datasets['broken_data']:
                [dict_training_set, dict_valid_set, dict_test_set] = self.split_dataset(data)
                [dict_training_set, dict_valid_set, dict_test_set] = [
                    self.clean_dataset(dict_training_set),
                    self.clean_dataset(dict_valid_set),
                    self.clean_dataset(dict_test_set)
                ]
                
                broken_data.append({
                        'name': data['name'],
                        'Ts': data['Ts'],
                        'frequency': data['frequency'],
                        'training': dict_training_set,
                        'valid': dict_valid_set,
                        'test': dict_test_set
                    })
                
                datasets = {
                    'healthy_data': healthy_data,
                    'broken_data': broken_data
                    }
                
                sio.savemat('split_datasets.mat', datasets)
                
                return True
                
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
# %% class SuportVectorClassification
class SupportVectorClassification(object):
    """
    This class applies SVM algorythms on a given training, valid and test dataset
    """
    def __init__(self):
        pass

    def use_linear_kernel(self,
                          penalty_of_error=0.1,
                          probability=True,
                          maximum_number_of_iterations=20000):
        """
        This method uses the linear classification method of the Support Vector Machine

        :param penalty_of_error: (Number) The penalty parameter C of the error term. (Default: 1)
        :param probability: (Boolean) Whether to enable probability estimates. This must be enabled prior to calling
        fit, and will slow down that method. (Default: True)
        :param maximum_number_of_iterations: (Integer) Hard limit on iterations within solver, or -1 for no limit.
        (Default: 20000)
        :return: (SVC) The SVC Linear model
        """
        try:
            return SVC(C=penalty_of_error,
                       kernel='linear',
                       probability=probability,
                       max_iter=maximum_number_of_iterations)
            
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def use_polynomial_kernel(self, penalty_of_error=0.1, degree=3, gamma='auto'):
        """
        This method uses the polynomial classification method of the Support Vector Machine

        :param penalty_of_error: (Number) The penalty parameter C of the error term. (Default: 1)
        :param degree: (Integer) The degree of the polynomial (Default: 3)
        :param gamma: (Number) Kernel coefficient (Default: 'auto')
        :return: (SVC) The SVC polynomial model
        """
        try:
            return SVC(C=penalty_of_error,
                       kernel='poly',
                       degree=degree,
                       gamma=gamma)

        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def use_radial_basis_function_kernel(self, penalty_of_error=0.1, gamma='auto'):
        """
        This method uses the radial basic function classification method of the Support Vector Machine

        :param penalty_of_error: (Number) The penalty parameter C of the error term. (Default: 1)
        :param gamma: (Number) Kernel coefficient (Default: 'auto')
        :return: (SVC) The SVC radial basic function model
        """
        try:
            return SVC(C=penalty_of_error,
                       kernel='rbf',
                       gamma=gamma)
            
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
        
    def get_predicted_output(self, model, dict_training_set, dict_valid_set):
        """
        This method returns the predicted output of a SVC model determined earlier with one of the 'use_linear_kernel', 
            'use_polynomial_kernel', or 'use_radial_basis_function_kernel' methods
            
        :param model: (SVC) The model returned by one of the methods metioned above
        :param dict_training_set: (Dictionary) A dictionary containing the training set features and targets
            {
                'X': <Numpy Array>,
                'y': <Numpy Array>
            }
        :param dict_valid_set: (Dictionary) A dictionary containing the validation set features and targets
            {
                'X': <Numpy Array>,
                'y': <Numpy Array>
            }
        :return: (Dictionary) A dictionary containing the SVC model fitted on the training set, the predicted output
            and the mean squared error between the validation targets and the predicted targets
            {
                'modle': <SVC model>,
                'y_predicted': <Numpy Array>,
                'error': <Number>
            }
        """
        try:
            model.fit(X=dict_training_set['X'], 
                      y=(dict_training_set['y']))
            y_predicted = model.predict(dict_valid_set['X'])
            
            return {
                    'model': model,
                    'y_predicted': y_predicted,
                    'error': mean_squared_error(dict_valid_set['y'], y_predicted)
                    }
            
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def get_classification_report(self, y_real, y_predicted):
        """
        This method returns on the console the classification report for the real and predicted targets 
        
        :param y_real: (Numpy Array) A column vector containing the real target values
        :param y_predicted: (Numpy Array) A column vector containig the predicted target values
        :return: (String) The classification report
        """
        try:
            return classification_report(y_real, y_predicted)
        
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
    def get_confusion_matrix(self, y_real, y_predicted):
        """
        This method returns on the console the confusion matrix for the real and predicted targets 
        
        :param y_real: (Numpy Array) A column vector containing the real target values
        :param y_predicted: (Numpy Array) A column vector containig the predicted target values
        :return: (String) The confusion matrix
        """
        try:
            return confusion_matrix(y_real, y_predicted)
        
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    
# %% Exports
dataset = Dataset()
support_vector_classification = SupportVectorClassification()

