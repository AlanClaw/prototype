import logging
_logger = logging.getLogger(__name__)

class MovieDownloadSpider(object):

    _movie_list = None
    
    def __init__(self):
        pass

if __name__ == '__main__':
    '''
    '''
    logging.basicConfig(
        format = '[%(asctime)s] %(levelname)s [%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%y-%m-%d %H:%M:%S'
    )