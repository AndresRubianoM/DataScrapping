import argparse
import logging
from urllib.parse import urlparse
import pandas as pd 
import hashlib
import nltk
from nltk.corpus import stopwords

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
 
def main(filename):
    logger.info('Begining the cleaning process')
    df = _read_data(filename)

    #Cleaning the dataframe 
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_newline_for_body(df)
    df = _remove_duplicate_entries(df)
    df = _drop_rows_with_missing_data(df)

    #Adding new info
    df = _add_tokens(df)
    return df

def _read_data(filename):
    logger.info('Reading the data file {}'.format(filename))
    return pd.read_csv(filename)
    
def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]
    logger.info('Newspaper uid detected: {}'.format(newspaper_uid))
    return newspaper_uid

def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('Filling newspaper uid column with: {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid
    return df

def _extract_host(df):
    logger.info('Extracting the host')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df

def _fill_missing_titles(df):
    logger.info('Filling the missing titles')
    missing_titles_mask = df['title'].isna()
    missing_titles = (df[missing_titles_mask]['url']
                    .str.extract(r'(?P<missing_titles>[^/]+)$')
                    .applymap(lambda title: title.split('-'))
                    .applymap(lambda words_list: ' '.join(words_list)))
    
    df.loc[missing_titles_mask, ['title']] = missing_titles['missing_titles']

    return df

def _generate_uids_for_rows(df):
    logger.info('Generating uid for each news')
    uids = (df.apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis = 1)
            .apply(lambda hash_object: hash_object.hexdigest()))
    
    df['uid'] = uids
    return df.set_index('uid')

def _remove_newline_for_body(df):
    logger.info('Cleaning the body of each news')
    stripped_body = (df.apply(lambda row: row['body'].replace('\n', ' ').replace('\r', ' ').replace('\xa0', ' '), axis = 1))
    df['body'] = stripped_body
    return df

def _remove_duplicate_entries(df):
    logger.info('Removing the duplicates')
    columns_remove_duplicates = ['title', 'body']
    
    df.drop_duplicates(subset = columns_remove_duplicates, keep = 'first', inplace = True)
    return df 

def _drop_rows_with_missing_data(df):
    logger.info('Removing rows with missing data')
    return df.dropna()

def _add_tokens(df):
    logger.info('Counting the number of stop words in specific columns')
    #stop words are the words differents of articles
    stop_words = set(stopwords.words('spanish'))
    columns_to_tokenize = ['title', 'body']
    for column in columns_to_tokenize:
        df['n_tokens_{}'.format(column)] = _tokenizer(df, column, stop_words)
   

    return df

def _tokenizer(df, column, stop_words):
    return (df.dropna()
    .apply(lambda row: nltk.word_tokenize(row[column]), axis = 1)               #Convert the strings to tokens
    .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))  #test if the token isnt nan and if is alphabetic
    .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))       #Convert each token in lower case
    .apply(lambda words_lists: list(filter(lambda word: word not in stop_words, words_lists))) #Confirms if the word is in the list of stopwords
    .apply(lambda valid_word_list: len(valid_word_list)))

def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename)
    logger.info('Saving the data in {}'.format(clean_filename))
    df.to_csv(clean_filename)

 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                         help = 'Path to the dirty data',
                         type = str)
     
    arg = parser.parse_args()
    df = main(arg.filename)
    _save_data(df, arg.filename)
