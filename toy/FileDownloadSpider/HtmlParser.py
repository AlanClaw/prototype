import logging
_logger = logging.getLogger(__name__)

import urllib2
from HTMLParser import HTMLParser
# from lxml import html

def main():
    """
    """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
    
    content = urllib2.urlopen("http://notepad-plus-plus.org/download").read()
    parser = HtmlLinkParser()
    link = []
    parser.feed(content)
    
    link = parser.get_all_href_value()
    print link
#     get_link()
    parser.close()

class HtmlLinkParser(HTMLParser):
    
    href_value = None
    
    def __init__(self):
        
        HTMLParser.__init__(self)
    
        if self.href_value is None:
            self.href_value = []
        
    def handle_starttag(self, tag, attrs):
        
        
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
#                     print name, "=", value
                    self.href_value.append(value)
                    
    def get_all_href_value(self):
        """
        @rtype: []
        """
        return self.href_value
        
if __name__ == '__main__':
    main()