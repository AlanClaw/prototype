import logging
_logger = logging.getLogger(__name__)

class MoiveNameScout(object):
    
    def __init__(self):
        pass

    @property
    def config(self):
        return self._config
    
    @config.setter
    def config(self, value):
        pass

if __name__ == '__main__':
    '''
    '''
    logging.basicConfig(
        format = '[%(asctime)s] %(levelname)s [%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%y-%m-%d %H:%M:%S'
    )