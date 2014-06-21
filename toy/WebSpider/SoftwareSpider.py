import logging
_logger = logging.getLogger(__name__)

import os
import ConfigParser, urllib2, re
from HtmlParser import HtmlLinkParser

def main():
    """
    """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
    
    sft_spider = SoftwareSpider('software.ini', 'bbb')
    software = 'SystemExplorer_portable'
    sft_spider.get_download_link(sft_spider.get_ini_reader.get(software, 'download_page'), 
                                 sft_spider.get_ini_reader.get(software, 'download_link_ptn'))
'''
'''
class SoftwareSpider(object):
    """
    @note: This class is aim to auto get software by a defined software pattern
    """
    
    _sft_ini = None
    _sft_dir = None
    _config = None
    
    def __init__(self, _sft_ini, _sft_dir = None):
        """
        """
        self._sft_ini = _sft_ini
        self._sft_dir = _sft_dir

    def run(self):
        """
        """
        # check all the softwares from base folder to see if need download or not
        # download all the software from list and show the status 
        
        for sft_name in self.get_ini_reader.sections():
            
            # from page to find out target download link
            # create thread to download the software to '_sft_dir'
            url = self.get_ini_reader.get(sft_name, "download_page")
            url_ptn = self.get_ini_reader.get(sft_name, "download_link_ptn")
            download_link = self.get_download_link(url, url_ptn)
            if self.get_ini_reader.get(sft_name, "download_link_ptn"):
                pass
            
            _logger.debug("dwonload_link: %s" %download_link)
    
    @property
    def get_ini_reader(self):
        
        if self._config is None:
            self._config = ConfigParser.SafeConfigParser()
            self._config.optionxform = str
            self._config.read(self._sft_ini)
        
        return self._config
        
    def get_download_link(self, url, link_ptn):
        """
        """
        _logger.debug("url:%s\nsearch download pattern:%s" %(url, link_ptn))
        
        # get content from page and filter links
        links = self._parse_download_link(url)
        
        # find target link from all links
        re_format = re.compile(link_ptn)
        
        matchs = [link for link in links if re_format.match(link) is not None]

        _logger.debug("Match links:")
        _logger.debug(matchs)
        
        assert len(matchs) == 1, "Unique link not found!!"
        
        return matchs[0]
    
    def _parse_download_link(self, url):
        
        from bs4 import BeautifulSoup
        
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read(), 'html5lib')
        links = soup.findAll('a')
        all_links = []
        
        for link in links:
            try:
                _logger.debug("link string:%s" %link.string)
                _logger.debug(link['href'])
                all_links.append(link['href'])
            except:
                logging.exception('_parse_download_link')
                
        return all_links
    
    def compare_software_version(self, sft_name1, sft_name2):
        """
        @note: Implement this if needed
        """
        return NotImplementedError
    
def get_desktop_path():
    """
    HKEY_CURRENT_USER
    """
    import _winreg

    desktop_path = ""

    aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
    aKey = _winreg.OpenKey(aReg, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")

    try:
        val= _winreg.QueryValueEx(aKey, "Desktop")            
        _logger.debug("reg key value:%s" %str(val))
        desktop_path = str(val[0])
        
    except EnvironmentError:
        print traceback.format_exc()
        print sys.exc_info()[0]       

    return desktop_path

def download_file():
    
    import urllib2
    
    download_file = urllib2.urlopen('http://download.tuxfamily.org/notepadplus/6.6.4/npp.6.6.4.Installer.exe')
    
    file_path = os.path.join(get_desktop_path(), "npp.6.6.4.Installer.exe")
    _logger.debug("file_path = %s" %file_path)
    with open(file_path, 'wb') as output:
        output.write(download_file.read())



if __name__ == "__main__":
    main()