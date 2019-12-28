# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 16:50:11 2019

@author: Dan Alexandru-Bogdan
"""
# %% Imports
from globals import console
from tkinter.filedialog import askopenfilename
from random import randrange
import glob
import os
import ntpath

import pandas as pd
import numpy as np


# %% class Dataset
class Dataset(object):
    """
    This class deals with the datasets 
    """
    def __init__(self):
        self.csvs_folder = {
        'main': 'csvs',
        'healthy_data': 'csvs/Healthy Data',
        'brokentooth_data': 'csvs/BrokenTooth Data'
        }
        self.csv_filenames = {}

    
    def get_dataset(self, path=None):
        """
        This method returns the dataset of a csv file
        
        :param path: (String) The path of the csv file
        :return: (Dictionary) A Dictionary containing the dataset, and the features of that csv file
            {
                'name': <String>,
                'X': <Numpy Array>,
                'y': <Numpy Array>
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
                    'y': y
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
            brokentooth_data_filenames = glob.glob(self.csvs_folder['brokentooth_data'] + '/*.csv')
            
            self.csv_filenames = {
                    'healthy_data': healthy_data_filenames,
                    'broken_data': brokentooth_data_filenames
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
                        'name': <String>
                        'X': <Numpy Array>,
                        'y': <Numpy Array>
                    }],
                    'broken_data': [
                    {
                        'name': <String>
                        'X': <Numpy Array>,
                        'y': <Numpy Array>
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
    
    
dataset = Dataset()
