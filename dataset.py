# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 16:50:11 2019

@author: Dan Alexandru-Bogdan
"""
# %% Imports
from globals import console
from tkinter.filedialog import askopenfilename
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
        pass
    
    
    def get_dataset(self, path=None):
        """
        This method returns the dataset of a csv file
        
        :param path: (String) The path of the csv file
        :return: (Dictionary) A Dictionary containing the dataset, and the features of that csv file
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
                y = np.zeros((X.size, 1))
            elif 'broken' in str(path).lower():
                y = np.ones((X.size, 1))
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
        
        
dataset = Dataset()
