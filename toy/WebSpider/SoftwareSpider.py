import logging
_logger = logging.getLogger(__name__)

import os
import ConfigParser, urllib2, re

def main():
    """
    """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
    
    SoftwareSpider('aaa', 'bbb').parse_html("sss")
#     SoftwareSpider('aaa', 'bbb').\
#         get_link( "http://notepad-plus-plus.org/download", 
#                   "^http://download.tuxfamily.org/notepadplus*Installer.exe$" )
#     get_page_content()
    

class SoftwareSpider(object):
    """
    @note: This class is aim to auto get software by a defined software pattern
    """
    
    sft_ini = None
    sft_base_dir = None
    
    def __init__(self, sft_ini, sft_base_dir = None):
        """
        """
        self.sft_ini = sft_ini
        self.sft_base_dir = sft_base_dir

    def run(self):
        """
        """
        # check all the softwares from base folder to see if need download or not
        # download all the software from list and show the status 
        config = ConfigParser.SafeConfigParser()
        config.optionxform = str
        config.read(self.sft_ini)
        
        for sft_name in config.sections():
            
            # from page to find out target download link
            # create thread to download the software to 'sft_base_dir'
            
            url = config.get(sft_name, "download_page")
            url_ptn = config.get(sft_name, "download_link_ptn")
            download_link = self.get_download_link(url, url_ptn)
            _logger.debug("dwonload_link: %s" %download_link)
    
    def get_link(self, url, link_ptn):
        """
        """
        _logger.debug("url:%s\nsearch download pattern:%s" %(url, link_ptn))
        
        link = ""
        content = urllib2.urlopen(url).read()
        
        pattern = re.compile(link_ptn)
        match = pattern.match(content)
        
        assert match is not None, "Link not found"
        _logger.debug(match.group(0))
        
        return link
    
    
    def parse_html(self, page_content):
        """
        """
        pass
    
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