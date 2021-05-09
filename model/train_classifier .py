import sys
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# import libraries
import pandas as pd
import numpy as np
from nltk import word_tokenize
import sqlite3
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline,FeatureUnion
from sqlalchemy import create_engine
from nltk.stem import WordNetLemmatizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.externals import joblib

def load_data(database_filepath):
    # load data from database
    engine = create_engine('sqlite:///disaster_response.db')
    df = pd.read_sql_table('disaster_response', engine)
    X = df['message']
    Y = df.drop(columns= ['id','message', 'original', 'genre'])
    return X, Y, Y.columns

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
def tokenize(text):
    """
    tokenize, lemmanize, normalization,strip, removal of stop words
    from the text
    """
    # Detect URLs
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, 'urlplaceholder')
    # Normalize and tokenize and remove punctuation
    tokens = nltk.word_tokenize(re.sub(r"[^a-zA-Z0-9]", " ", text.lower()))
     # Remove stopwords
    tokens = [t for t in tokens if t not in stopwords.words('english')]
  
      # Lemmatize
    lemmatizer=WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
   
    return tokens

class TextLengthExtractor(BaseEstimator,TransformerMixin):
    """
    An estimator that count the text length of each cell in the X
    """
    def fit(self, X, y= None):
        """
        return self
        """
        return self
    def transform(self,X):
        """
        count the length of each cell in the X
        """
        X_length = pd.Series(X).str.len()
        
        return pd.DataFrame(X_length)

def build_model():
    """
    Build pipeline with Tfidf, length of text and OneVsRestClassifier and GridSearchCV
    """
    pipeline = Pipeline([
        ('feature', FeatureUnion([
            ('text_pipeline', Pipeline([
                ('vect', CountVectorizer(tokenizer = tokenize)),
                ('tfidf', TfidfTransformer())])),
            ('text_len', TextLengthExtractor())
        ])),
        ('clf', MultiOutputClassifier(OneVsRestClassifier(MultinomialNB( fit_prior=True,              class_prior=None)))),])
    
    # Set up the search grid
    parameters = {'feature__text_pipeline__tfidf__use_idf': (True,False),
                   'clf__estimator__estimator__alpha': (1e-2, 1e-3)
    }
    
    # Initialize GridSearch cross validation object
    cv = GridSearchCV(pipeline, param_grid=parameters)

    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    
    '''
    Evaluate the model performance of each category target column
    '''
    # use model to predict
    Y_pred = model.predict(X_test)
    # Turn prediction into DataFrame
    Y_pred = pd.DataFrame(Y_pred,columns=category_names)
    # For each category column, print performance
    for col in category_names:
        print(f'Column Name:{col}\n')
        print(classification_report(Y_test[col],Y_pred[col]))


def save_model(model, model_filepath):
    '''
    Save model to a pickle file
    '''
    joblib.dump(model, model_filepath) 


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()