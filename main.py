#Import modules
import argparse
import re 
##Module to show the messages on the cmd
import logging
##Import posible errors
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

#Import from files
from common import config 
import news_page_objects as news


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'^https?://.+/.+$') #example: http or https ://example.com/example1
is_root_path = re.compile(r'/.+$') #example: /example 


def _news_scraper(news_site_uid):
    ''' Function that manage the main logic for the scraper'''

    #Defining wich news page is going to be scrape
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('Beginning scraper for {}'.format(host))
    homepage = news.HomePage(news_site_uid, host)

    articles = []

    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info('Article fetched')
            articles.append(article)
            print(article.title)
        
    print(len(articles))



def _fetch_article(news_site_uid, host, link):
    logger.info('Starting fetching at article {}'.format(link))
    article = None

    #Check if the article exists 
    try:
        article = ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info = False)
        pass
    
    #Filter if the article have a body 
    if article and not article.body:
        logger.warning('Invalid article. Theres no body')
        return None 
    else:
        return article 


def _build_link(host, link):
    ''' The function supervised if the link is complete by itself or it need to be complete it '''

    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{}/{}'.format(host, link)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #Import the sites of config.yaml 
    news_sites_choices = list(config()['news_sites'].keys())

    parser.add_argument('news_site', 
                        help = 'The news site that you want to scrape',
                        type = str,
                        choices = news_sites_choices)
    
    args = parser.parse_args()
    _news_scraper(args.news_site)