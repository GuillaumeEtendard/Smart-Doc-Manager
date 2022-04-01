"""
This module is to train the model to classify if the file is a cv or an invoice.
"""
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import pickle

def preprocessing(df):
    """
    df : dataframe 
    Returns : Ndarray - the dataframe preprocessed split into train and validation set 
    """

    target = df['label'].values
    text_features = df['cleaned_data'].values
    word_vectorizer = TfidfVectorizer(sublinear_tf=True,stop_words='english',max_features=266)
    word_vect = word_vectorizer.fit(text_features)
    WordFeatures = word_vect.transform(text_features)
    X_train, X_test, y_train, y_test = train_test_split(WordFeatures, target, random_state=42, test_size =0.2, shuffle = True, stratify = target)
    return X_train,X_test,y_train,y_test

def model(df):
    """
    df : dataframe 
    Returns : model trained 
    """
    X_train,X_test,y_train,y_test = preprocessing(df)
    clf = OneVsRestClassifier(KNeighborsClassifier())
    clf.fit(X_train,y_train)
    return clf  

def save_model(filename,model):
    """
    This function save the model trained 
    filename : String filename
    model : model trained  
    """
    Pkl_Filename = filename +".pkl"
    with open(Pkl_Filename, 'wb') as file:  
        pickle.dump(model, file)

def load_model(filename):
    """
    This function load the model trained 
    filename : String - filename
    """
    Pkl_Filename= filename+".pkl"
    with open(Pkl_Filename, 'rb') as file:  
        model = pickle.load(file)
    return model 

def predict(model, df):
    """
    model : model pretrained
    df : dataframe
    Returns : prediction from the model trained on the test set
    """
    X_train,X_test,y_train,y_test = preprocessing(df)
    prediction  = model.predict(X_test)
    return prediction 

if __name__ == '__main__':
    filename = 'KNN_classifier'
    df = pd.read_csv('data_cleaned.csv')
    clf = model(df)
    save_model(filename,model)
    prediction = predict(model,df)&0