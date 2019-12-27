# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:09:17 2019

@author: Dan Alexandru-Bogdan
"""
# %% Imports
from globals import console
from get_csv_files import get_csv_files
from dataset import dataset


# %% Main
def main():
    """
    The function is the main section from which the project is being run

    :returns: Boolean (True or False)
    """
    try:
#        get_csv_files.run()
        data = dataset.get_dataset('csvs/Healthy Data/h30hz0.csv')
        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR)
        return False


if __name__ == '__main__':
    main()
