#Import modules
import requests
from bs4 import BeautifulSoup
#Import 
from common import config

class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        
        self._html = None
        self._visit(url)


    #Select the respective querie
    def _select(self, query_string):
        return self._html.select(query_string)


    #Make the request to the url 
    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()
        self._html = BeautifulSoup(response.text, 'lxml')



#Class that manage the Home page of the differents News pages
class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)
                

        return set(link['href'] for link in link_list)



#Class that manage each of the article pages
class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        self._url = url
        super().__init__(news_site_uid, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''


    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''

    @property
    def url(self):
        return self._url


        

    