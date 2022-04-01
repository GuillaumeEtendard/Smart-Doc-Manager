"""
This module is here to clean the  datasets.
"""

import os
import pandas as pd
import re
from nltk.tokenize import TweetTokenizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import pickle


def df_concatenate(df1, df2):
    """
    df1 : first dataframe
    df2 : second dataframe
    Returns : the dataframe concatenate
    """
    return pd.concat([df1, df2])


def Tostring(df):
    """
    df : dataframe
    Returns : dataframe with label & raw data as string type 
    """

    return df.applymap(str)


def cleaning_features(text, stopwords):
    """
    text : raw text to clean
    stopwords : list of english stopwords
    Returns : text preprocessed 
    """

    text = re.sub('#\S+', '', text)
    text = re.sub('@\S+', '  ', text)
    text = re.sub('[%s]' % re.escape(
        """!"#$%&'()*+,-./:;<=>?@[\]^'{|}~"""), ' ', text)
    text = re.sub(r'[^\x00-\x7f]', r' ', text)
    text = re.sub('\n+', ' ', text)

    tokenizer = TweetTokenizer()
    text = tokenizer.tokenize(text)
    text_lower = [word.lower() for word in text]
    text_clean = [word for word in text_lower if (
        word not in stopwords and len(word) > 2)]

    return text_clean


def cleaning_full(df_cv, df_invoice, stopwords):
    """
    df_cv : dataframe containing cv 
    df_invoice : dataframe containing invoice
    text : raw text to clean
    stopwords : list of english stopwords
    Returns : dataframe preprocessed 
    """
    df = df_concatenate(df_cv, df_invoice)
    df = Tostring(df)
    df['cleaned_data'] = df.raw.apply(
        lambda x: cleaning_features(x, stopwords_english))
    print(df['cleaned_data'][1])
    df['cleaned_data'] = df['cleaned_data'].apply(lambda x: ' '.join(x))
    print(df['cleaned_data'][1])

    df.to_csv('data_clean.csv', index=False)

    print('cleaning full print first row', df['cleaned_data'][1])

    return df


def preprocessing(df):
    """
    df : dataframe 
    Returns : Ndarray - the dataframe preprocessed split into train and validation set 
    """

    target = df['label'].values
    text_features = df['cleaned_data'].values
    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True, stop_words='english', max_features=266)
    word_vect = word_vectorizer.fit(text_features)
    WordFeatures = word_vect.transform(text_features)
    X_train, X_test, y_train, y_test = train_test_split(
        WordFeatures, target, random_state=42, test_size=0.2, shuffle=True, stratify=target)

    return X_train, X_test, y_train, y_test


def model(df):
    """
    df : dataframe 
    Returns : model trained 
    """
    X_train, X_test, y_train, y_test = preprocessing(df)
    clf = OneVsRestClassifier(KNeighborsClassifier())
    clf.fit(X_train, y_train)
    return clf


def save_model(filename, model):
    """
    This function save the model trained 
    filename : String filename
    model : model trained  
    """
    Pkl_Filename = filename + ".pkl"
    with open(Pkl_Filename, 'wb') as file:
        pickle.dump(model, file)


if __name__ == '__main__':
    filename = 'KNN_classifier'
    df_cv = pd.read_csv('data_cv.csv')
    df_invoice = pd.read_csv('data_invoice.csv')
    stopwords_english = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                         "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    df_clean = cleaning_full(df_cv, df_invoice, stopwords_english)
    X_train, X_test, y_train, y_test = preprocessing(df_clean)
    clf = model(df_clean)
    save_model(filename, model)
