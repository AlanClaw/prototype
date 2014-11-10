import logging
_logger = logging.getLogger(__name__)

def get_utf8_value(value):
    """
    """
    msg = ''.join(value).encode('utf-8').strip()
    msg = msg.replace(' ', '')
    
    return msg.strip()

if __name__ == "__main__":
    pass