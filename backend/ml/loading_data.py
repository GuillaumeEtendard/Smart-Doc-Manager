"""
This module is here to handle the load the necessary datasets.
"""

import os
import pandas as pd 
import pytesseract
from pdfminer.high_level import extract_text
import docx
import docx2txt


def pdf_cv_to_text(df,cv_path,list_cv):
    """
    This function extract all the text from all the cv and append the raw data on the dataframe. 

    df : empty dataframe containing the columns label & raw data
    cv_path : string - path of the cv files 
    list_cv : list of string - containing all cv as pdf files
    
    Returns : df - dataframe containing all the cv extracted into text format
    """
    for idx in range(len(list_cv)):
        pdf_file = os.listdir(os.path.join(cv_path,'pdf'))[idx]
        raw_features = extract_text(os.path.join(cv_path,'pdf/',pdf_file))
        df = df.append({'label':'CV',
                        'raw': raw_features
                       },ignore_index=True)
    return df


def pdf_invoice_to_text(df,factures_path,list_type_invoice):
    """
    This function extract all the text from all the invoice and append the raw data on the dataframe. 

    df : dataframe containing the columns label & raw data
    factures_path : string - path of the invoice files 
    list_type_invoice : list of string - containing all the type of invoice
    
    Returns : df - dataframe containing all the invoice extracted into text format
    """
    for types in list_type_invoice :
        list_invoice = os.listdir(factures_path+'/'+types)
        for idx in range(len(list_invoice)):
            pdf_file = os.listdir(os.path.join(factures_path,types))[idx]
            raw_features = extract_text(os.path.join(factures_path,types,pdf_file))
            df = df.append({'label':'factures',
                            'raw': raw_features
                           },ignore_index=True)
    return df

def saving_dataset(df,name):
    """
    df : dataframe containing the dataset 
    name : name of the file saved
    Returns : dataframe save as a csv file 
    """
    return df.to_csv(name+'.csv',index=False)

if __name__ == '__main__':
    root = './data'
    factures_path = './data/Factures'
    cv_path = './data/CV/'

    list_cv = os.listdir(os.path.join(cv_path,'pdf'))
    list_type_invoice = os.listdir(factures_path)

    df = pd.DataFrame(columns =['label','raw'])
    
    df_cv = pdf_cv_to_text(df,cv_path,list_cv)
    df_invoice =pdf_invoice_to_text(df,factures_path,list_type_invoice)

    saving_dataset(df_cv,'data_cv')
    saving_dataset(df_invoice,'data_invoice')