import logging
_logger = logging.getLogger(__name__)

import os, ConfigParser, re, shutil
import urlparse, urllib, urllib2


"""
@attention: Please have the following dependence module to execute this program
easy_install html5lib
easy_install BeautifulSoup4
pip install requests 
"""

def main():
    """
    """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
    
    fld_path = os.path.join(os.environ['userprofile'], 'Desktop', 'test_dir')
    
    sft_spider = SoftwareSpider('software.ini', fld_path)
    sft_spider.run()
    

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
        
        if self._sft_dir is None:
            self._sft_dir = self._get_desktop_path()
        

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
            
            download_link = self.get_download_link(sft_name, url, url_ptn)
            _logger.debug("dwonload_link: %s" %download_link)

            self._download_file(download_link)
            
    @property
    def get_ini_reader(self):
        
        if self._config is None:
            self._config = ConfigParser.SafeConfigParser()
            self._config.optionxform = str
            self._config.read(self._sft_ini)
        
        return self._config
        
    def get_download_link(self, sft, url, link_ptn):
        """
        """
        _logger.debug("url:%s\nsearch download pattern:%s" %(url, link_ptn))
        
        # get content from page and filter links
        matchs = self._parse_link(url, link_ptn)
        if len(matchs) != 1:
            _logger.debug("match links:")
            _logger.debug(matchs)
            print "Multiple links found!! Choose the first one..."
            
        download_link = matchs[0]

        if self.get_ini_reader.has_option(sft, "dwonload_link_host"):
            download_link = self.get_ini_reader.get(sft, "dwonload_link_host") + download_link
        
        if self.get_ini_reader.has_option(sft, "redirect_link_ptn"):
            redirect_ptn = self.get_ini_reader.get(sft, "redirect_link_ptn")
            matchs = self._parse_link(download_link, redirect_ptn)
            assert len(matchs) == 1, "Unique redirect link not found!!"
            download_link = self.get_ini_reader.get(sft, "dwonload_link_host") + matchs[0]
            
        return download_link
    
    def _parse_link(self, url, ptn):
        
        from bs4 import BeautifulSoup
        
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read(), 'html5lib')
        links = soup.findAll('a')
        all_links = []
        
        for link in links:
            try:
#                 _logger.debug("link string:%s" %link.string)
#                 _logger.debug(link['href'])
                all_links.append(link['href'])
            except:
                logging.exception('_parse_link fail')
                
        # find target link from all links
        re_format = re.compile(ptn)
        matchs = [link for link in all_links if re_format.match(link) is not None]
        
        _logger.debug("Match links:")
        _logger.debug(matchs)

        return matchs
#         return all_links
    
    def _get_desktop_path(self):
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

    def _download_file(self, url, file_name = None):
        """
        @note: Used to downlaod file from url link
        """
        # check folder exist or not
        if not os.path.isdir(self._sft_dir):
            os.makedirs(self._sft_dir)
        
        request_url = urllib2.urlopen(urllib2.Request(url))
        download_file = urllib2.urlopen(url)
        
        try:
            file_name = file_name or self._get_file_name(url, request_url)
            file_path = os.path.join(self._sft_dir, file_name)
            _logger.debug("download to path = %s" %file_path)
            
            with open(file_path, 'wb') as fout:
                shutil.copyfileobj(request_url, fout)
        finally:
            request_url.close()

    def _get_file_name(self, url, openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(), ''),
                openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        
        # if no filename was found above, parse it out of the final URL.
        name = os.path.basename(urlparse.urlsplit(openUrl.url)[2])
        return urllib.unquote(name).decode('utf8')

    def _get_redirected_url(self, url):
        import requests
        
        response = requests.get(url)
        if response.history:
            _logger.debug("Request was redirected")
            for resp in response.history:
                _logger.debug(resp.status_code, resp.url)
            _logger.debug("Final destination:")
            _logger.debug(response.status_code, response.url)
        else:
            _logger.debug("Request was not redirected")

    def compare_software_version(self, sft_name1, sft_name2):
        """
        @note: Implement this if needed
        """
        return NotImplementedError

if __name__ == "__main__":
    main()