import logging 
import subprocess

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

news_sites_uid = ['elpais']


def main():
    _extract()
    _tranform()
    _load()

def _extract():
    logger.info('Beginning the extract process')

    for new_site_uid in news_sites_uid:
        #Commands to automatizate the cmd operations
        subprocess.run(['python', 'main.py', new_site_uid], cwd = '.\extract') #execute main.py to extract the data 
        subprocess.run(['move', '.\extract\*.csv', '.\Transform\{}_.csv'.format(new_site_uid)], shell = True) #Find all the files and move it 

def _tranform():
    logger.info('Starting transform process')

    for new_site_uid in news_sites_uid:
        dirty_data_filename = '{}_.csv'.format(new_site_uid)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)

        subprocess.run(['python', 'newspaper_recipe.py', dirty_data_filename], cwd = '.\Transform') #execute the newspaper_recipe.py
        subprocess.run(['del', '.\Transform\{}'.format(dirty_data_filename)], shell = True)
        subprocess.run(['move', '.\Transform\{}'.format(clean_data_filename), '.\load\{}.csv'.format(new_site_uid)], shell = True)


def _load():
    logger.info('Starting load process')

    for new_site_uid in news_sites_uid:
        clean_data_filename = '{}.csv'.format(new_site_uid)

        subprocess.run(['python', 'save_data.py', clean_data_filename], cwd = '.\load')
        subprocess.run(['del', '.\load\{}'.format(clean_data_filename)], shell = True)





if __name__ == '__main__':
    main()