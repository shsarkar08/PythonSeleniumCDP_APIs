from selenium.webdriver.support.events import EventFiringWebDriver,AbstractEventListener
import time
import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class BypassSSLCertTest(unittest.TestCase):

    _URL = 'https://untrusted-root.badssl.com/'

    def setUp(self):
        # self.chrome_options = Options()
        # self.chrome_options.set_capability('acceptInsecureCerts',True)
        # self.chrome_options.add_argument('ignore-certificate-errors')
        self.svc = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.svc)

        ''' Enable/disable whether all certificate errors should be ignored '''

        self.driver.execute_cdp_cmd('Security.setIgnoreCertificateErrors',{'ignore':True})

    def test_bypass_cert_err(self):

        driver = self.driver
        driver.get(self._URL)
        if 'error' in driver.title:
            try:
                err_text = driver.find_element(By.XPATH,"*//div[@id='error-code']")
                print("{} : {}".format(driver.title,err_text.get_attribute('innerHTML')))
                # Privacy error : net::ERR_CERT_AUTHORITY_INVALID
            except Exception as e:
                print(e)
        else:
            print("{} -> {}".format(driver.title,'SSL Cert Error Bypassed'))
            driver.save_screenshot('./ssl_cert.png')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
