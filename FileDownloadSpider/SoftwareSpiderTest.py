import logging
_logger = logging.getLogger(__name__)

import unittest
from SoftwareSpider import SoftwareSpider as SoftwareSpider

class SoftwareSpiderTest(unittest.TestCase):
       
    
    def test_get_notepad_plus_link(self):
        
        inst = SoftwareSpider('software.ini', '.')
        
        dwn_link = inst.get_download_link( inst.get_ini_reader.get('notepad++', 'download_page'), 
                                           inst.get_ini_reader.get('notepad++', 'download_link_ptn'))
        
        self.assertEqual(dwn_link, 
                         r"http://download.tuxfamily.org/notepadplus/6.6.6/npp.6.6.6.Installer.exe", 
                         "pattern error")
    
    def test_get_firefox_link(self):
        
        inst = SoftwareSpider('software.ini', '.')
        
        dwn_link = inst.get_download_link( inst.get_ini_reader.get('firefox', 'download_page'), 
                                           inst.get_ini_reader.get('firefox', 'download_link_ptn'))
        
        _logger.debug("dwn_link = %s" %dwn_link)
        self.assertEqual(dwn_link, 
                         r"https://download.mozilla.org/?product=firefox-30.0&os=win&lang=en-US", 
                         "pattern error")

        
if __name__ == "__main__":
    unittest.main()