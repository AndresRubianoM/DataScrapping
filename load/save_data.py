import argparse
import logging
import pandas as pd

from article import Article
from base import Base, Engine, Session

logging.basicConfig( level = logging.INFO)
logger = logging.getLogger(__name__)

def main(filename):
    Base.metadata.create_all(Engine)
    session = Session()
    articles = pd.read_csv(filename)

    for index, row in articles.iterrows():
        logger.info('Loding article uid {} into DB'.format(row['uid']))
        article = Article(row['uid'], 
                          row['body'], 
                          row['host'],
                          row['title'], 
                          row['newspaper_uid'],
                          row['n_tokens_body'],
                          row['n_tokens_title'], 
                          row['url'])
        
        session.add(article)
    
    session.commit()
    session.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                    help = 'Name of the filename that you want to save in the database',
                    type = str)
    
    args = parser.parse_args()
    main(args.filename)

