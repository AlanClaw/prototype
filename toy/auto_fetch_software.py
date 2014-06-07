import logging
_logger = logging.getLogger(__name__)


def main():
    pass

if __name__ == "__main__":
    
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.INFO,
        datefmt = '%m/%d/%y %H:%M:%S'
    )

    main()