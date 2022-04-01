"""
This module inference use the model pretrained to classify if the file is a cv or an invoice.
"""
import os
import pandas as pd
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

from .cleaning_data import cleaning_features, model


def pdf_cv_to_text(df, cv_path, list_cv):
    """
    This function extract all the text from all the cv and append the raw data on the dataframe. 

    df : empty dataframe containing the columns label & raw data
    cv_path : string - path of the cv files 
    list_cv : list of string - containing all cv as pdf files

    Returns : df - dataframe containing all the cv extracted into text format
    """
    for idx in range(len(list_cv)):
        pdf_file = os.listdir(os.path.join(cv_path, 'pdf'))[idx]
        raw_features = extract_text(os.path.join(cv_path, 'pdf/', pdf_file))
        df = df.append({'label': 'CV',
                        'raw': raw_features
                        }, ignore_index=True)
    return df


def load_model(filename):
    """
    This function load the model trained 
    filename : String - filename
    """
    Pkl_Filename = filename + ".pkl"
    with open(Pkl_Filename, 'rb') as file:
        model = pickle.load(file)
    # loaded_model = pickle.load(open(Pkl_Filename,'rb'))
    return model  # loaded_model


def predict(model, path, stopwords):
    """
    model : model pretrained
    filename : string - filename 
    Returns : prediction from the model trained on the test set
    """

    text = extract_text(path)
    text_clean = cleaning_features(text, stopwords)
    text_features = [' '.join(text_clean)]

    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True, stop_words='english', max_features=len(text_clean))
    word_vectorizer.fit(text_features)
    WordFeatures = word_vectorizer.transform(text_features)

    prediction = model.predict(WordFeatures)
    return prediction


def predict_from_file(path):
    model_name = 'Pickled_KNN'
    stopwords_english = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
                         "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it",
                         "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who",
                         "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
                         "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and",
                         "but", "if", "or", "because", "as",
                         "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
                         "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in",
                         "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
                         "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other",
                         "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s",
                         "t", "can", "will", "just", "don", "should", "now"]

    try:
        model = load_model(model_name)
        prediction = predict(model, path, stopwords_english)
        return prediction[0]
    except Exception as e:
        text = extract_text(path)
        text_clean = cleaning_features(text, stopwords_english)
        invoice_keywords = ['invoice', 'invoices', 'due',
                            'total', '€', '$', 'eur', 'usd', 'vat', 'tva']
        cv_keywords = ['cv', 'resume', 'email', 'university',
                       'education', 'qualification', 'nationality', 'work']
        invoice_counter = 0
        cv_counter = 0
        for kw in invoice_keywords:
            invoice_counter += sum(kw in s for s in text_clean)
        for kw in cv_keywords:
            cv_counter += sum(kw in s for s in text_clean)
        if cv_counter > invoice_counter:
            return 'CV'
        elif cv_counter < invoice_counter:
            return 'invoice'
        else:
            return None


if __name__ == '__main__':
    cv_filename = 'data/CV/pdf/11.pdf'
    invoice_filename = 'data/Factures/hotel/moxy_20191221_006.pdf'
    predict_from_file(invoice_filename)
