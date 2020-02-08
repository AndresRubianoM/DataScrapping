#Import modules
import requests
from bs4 import BeautifulSoup
#Import 
from common import config

class NewsPage:

    def __init__(self, news_site_uid, url):
        self.__config = config()['news_sites'][news_site_uid]
        self.__queries = self.__config['queries']
        
        self.__html = None
        self._visit(url)


    #Select the respective querie
    def _select(self, query_string):
        return self.__html.select(query_string)


    #Make the request to the url 
    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()
        self.__html = BeautifulSoup(response.text, 'lxml')



#Class that manage the Home page of the differents News pages
class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self.__queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)
        
        return set(link['href'] for link in link_list)



#Class that manage each of the article pages
class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def body(self):
        result = self._select(self.__queries(['article_body']))
        return result[0].text if len(result) else ''

    @property
    def title(self):
        result = self._select(self.__queries(['article_title']))
        return result[0].text if len(result) else ''


        

    