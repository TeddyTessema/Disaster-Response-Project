import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    load in message datasets and categories dataset
    """
    # load messages datasets
    messages = pd.read_csv(messages_filepath)
    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    
    # merge dataset
    df = messages.merge(categories, how = 'left', on = ['id'])
    
    return df

def clean_data(df):
    '''
    make split categories into separate category columns.
    convert categories values just 0 and 1
    replace categories column in df with new category columns
    removal of duplicates
    '''
    # create a dataframe of the 36 individual category columns
    categories = pd.DataFrame(df['categories'].str.split(';', expand = True))
    # use this first row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything 
    # up to the second to last character of each string with slicing
    category_colnames = categories.iloc[0].str.split('-').apply(lambda x: x[0])
    # rename the columns of `categories`
    categories.columns = category_colnames
    #- Iterate through the category columns in df to keep only 
    # the last character of each string (the 1 or 0)
    for column in categories:
        categories[column] = categories[column]\
        .astype(str).str.split('-').apply(lambda x:x[1])
        
        # convert column string into numerics
        categories[column] = categories[column].astype(np.int)
    
    # drop the original categories column from `df`
    df = df.drop('categories',axis = 1 )
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis = 1)
    # replace the value int 2 into int 1 due to small sample size
    df['related'] = df['related'].astype(str).str.replace('2', '1')
    df['related'] = df['related'].astype(np.int)
    # drop duplicates
    df = df.drop_duplicates()
    return df

def save_data(df, database_filename):
    '''
    Save data into database
    :param df: input data
    :param database_filename: disaster response
    '''
    #Save the clean dataset into an sqlite database
    table_name = 'labeled_messages'
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql(table_name, engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
    
    
