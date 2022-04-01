"""
This module is here to handle the download of the necessary datasets.

Requirements :

- accepts the rules of the competition
- have the API token inside your $HOME/.kaggle/ folder to be able to use the kaggle api `doc<https://www.kaggle.com/docs/api>`_

"""

import os
import zipfile
import kaggle

def download_data(competition_name, dataset_name, path):
    """
    This function download the dataset inside the list from a kaggle
    competition.

    - competition_name : name of the kaggle competition as a string
    - dataset_name :  name of dataset
    - path : path where the data will be saved
    """
    try:
        kaggle.api.authenticate()
    except OSError:
        print('Are you sure you have the Kaggle API token?')
    try:
        kaggle.api.competition_download_file(competition_name,dataset_name, path=path)
    except OSError:
        print('Did you accept the rules for the competition?')
    return True

def extract_data(zip_path, path):
    """
    This function extract the data inside a list of zip folder name.

    - zip_path : path of the zip folder to extract
    - path : the path where you want to extract the zip files
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipref:
            zipref.extractall(path)
        os.remove(zip_path)
    except OSError:
        print('Do the file listed in zip_path exist ?')
    return True

def make_data(competition_name, file, path,zip_path):
    """
    This function does the downloading and extracting step of the data.

    - competition_name : name of the kaggle competition as a string
    - file : file to download from dataset
    - path : path where the data will be saved
    - zip_path : path for the name of the zip folder to extract
    """
    download_data(competition_name, file, path)
    extract_data=(zip_path, path)
    return True


def downloading_data(dataset_name,path):
    try:
        kaggle.api.authenticate()
    except OSError:
        print('Are you sure you have the Kaggle API token?')
    
    kaggle.api.dataset_download_files('tomtea/smart-doc-manager', path=PATH)
    with zipfile.ZipFile(dataset_name, 'r') as zipref:
        zipref.extractall(PATH)
    os.remove(dataset_name)

if __name__ == '__main__':
    PATH = './'
    dataset_name = './smart-doc-manager.zip'

    COMPETITION_NAME = 'tomtea' 
    file = 'smart-doc-manager.zip'
    zip_path = './smart-doc-manager.zip'
    
    #make_data(COMPETITION_NAME, file, PATH,zip_path)
    downloading_data(dataset_name,PATH)
