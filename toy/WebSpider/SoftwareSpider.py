import logging
_logger = logging.getLogger(__name__)

import os

class FetchSoftware(object):
    """
    """
    
    def __init__(self):
        pass

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


def get_page_content():
    
    import urllib2
    content = urllib2.urlopen('http://notepad-plus-plus.org/download/v6.6.4.html').read()

    print content


def main():
    """
    """
    download_file()
    
if __name__ == "__main__":
    
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.INFO,
        datefmt = '%m/%d/%y %H:%M:%S'
    )

    main()