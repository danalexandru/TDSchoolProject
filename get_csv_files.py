# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:14:55 2019

@author: Dan Alexandru-Bogdan
"""

# %% Imports
from globals import console
import pandas as pd
import glob

# %% GetCsvFiles
class GetCsvFiles(object):
    """
    This class is used in order to convert txt files into csvs (if it is possible)
    """

    def __init__(self):
        self.csv_folder_name = 'csvs'
        self.gearboxdata_folders = {
                'main': 'gearboxdata',
                'healthy_data': 'gearboxdata/Healthy Data',
                'brokentooth_data': 'gearboxdata/BrokenTooth Data'}
        self.gearboxdata_columns = ['sensor 1', 'sensor 2', 'sensor 3', 'sensor 4']
        
    def get_csv_data(self, filename):
        """
        This method gets the content of a txt file

        :param filename: (String) The name of the file that needs to be converted into a csv
        :returns: (List) The csv data
        """
        try:
            # Get file rows
            csv_data = []
            with open(filename, 'r') as file:
                rows = file.read().split('\n')
                rows.remove('')
                
            # Convert row data into columns
            for row in rows:
                row = row.split('\t')
                row.remove('')
                
                for i in range(len(row)):
                    row[i] = float(row[i])
                
                csv_data.append(row)
                    
            return csv_data
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def save_as_csv(self, filename, csv_data):
        """
        This method saves the data taken from the txt file as a csv
        
        :param filename: (String) The name of the file that needs to be converted into a csv
        :param csv_data: (List) The data needed to be saved
        :returns: Boolean (True or False)
        """
        try:
            # Get the new filename
            csv_filename = filename
            csv_filename = csv_filename.replace(self.gearboxdata_folders['main'], 
                                                self.csv_folder_name)
            csv_filename = csv_filename.replace('txt', 'csv')
            
            # Save data as csv
            df = pd.DataFrame(data=csv_data, columns=self.gearboxdata_columns)
            df.to_csv(csv_filename, sep=',', index=False)
            
            return True
        except Exception as error_message:
            console.log(error_message, console.log(error_message, console.LOG_ERROR))
            return False
        
    def run(self):
        """
        This method gets all the txt filenames from a folder
        
        :returns: Boolean (True or False)
        """
        try:
            # Get filenames
            healthy_data_filenames = glob.glob(self.gearboxdata_folders['healthy_data'] + '/*.txt')
            brokentooth_data_filenames = glob.glob(self.gearboxdata_folders['brokentooth_data'] + '/*.txt')
            
            # Save healthy data files
            for filename in healthy_data_filenames:
                csv_data = self.get_csv_data(filename)
                self.save_as_csv(filename, csv_data)
                
            # Save healthy data files
            for filename in brokentooth_data_filenames:
                csv_data = self.get_csv_data(filename)
                self.save_as_csv(filename, csv_data)
                
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
    

get_csv_files = GetCsvFiles()
