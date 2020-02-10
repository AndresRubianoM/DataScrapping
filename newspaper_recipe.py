import argparse
import logging
from urllib.parse import urlparse
import pandas as pd 
import hashlib

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
 
def main(filename):
    logger.info('Begining the cleaning process')
    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_newline_for_body(df)

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
    
    df[missing_titles_mask]['title'] = missing_titles['missing_titles']

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












 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                         help = 'Path to the dirty data',
                         type = str)
     
    arg = parser.parse_args()
    df = main(arg.filename)

    print(df)