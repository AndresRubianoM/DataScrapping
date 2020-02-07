#Import modules
import argparse
##Module to show the messages on the cmd
import logging
logging.basicConfig(level = logging.INFO)
#Import from files
from common import config 


logger = logging.getLogger(__name__)



def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #Import the sites of config.yaml 
    news_sites_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site', 
                        help = 'The new site that you want to scrape',
                        type = str,
                        choices = news_sites_choices)
    
    args = parser.parse_args()
    _news_scraper(args.news_site)