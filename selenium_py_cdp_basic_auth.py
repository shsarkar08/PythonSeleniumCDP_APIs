from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import base64
import time
import unittest


class test_basic_auth(unittest.TestCase):

    _url = 'https://the-internet.herokuapp.com/basic_auth'

    def setUp(self):
        self.svc = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.svc)
        self.driver.maximize_window()
        '''
        Enable the Network & Pass Auth Headers using Chrome Devtools Protocol APIs
        '''
        self.driver.execute_cdp_cmd('Network.enable',{})
        self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders',self.header_data('admin','admin'))
        self.driver.get(self._url)

    def test_auth(self):
        try:
            self.succ_msg = self.driver.find_element(By.XPATH, '//p').get_attribute('textContent')
            assert 'Congratulations!' in self.succ_msg
            print(str(self.succ_msg).strip()) # Congratulations! You must have the proper credentials
        except NoSuchElementException as exep:
            print('Success Message Not Found, Basic Auth Test Fail')

    def header_data(self,username,password):
        '''
        header params to be passed as dict format
        :param username: username for login api
        :param password: password for login api
        :return: Base64 encoded strig representation, appended to the text "Basic"
        '''
        _auth_header = {'headers':{
            'Authorization': 'Basic '+ self.encode_bs64(username,password)
        }}
        return _auth_header

    def encode_bs64(self,username,password):
        '''
        Username:Password encoding to Base64
        :param username: username for login api
        :param password: password for login api
        :return: Base64 encoded string
        '''
        _auth = username + ":" + password
        _au_byte_obj = _auth.encode('ascii')
        _base64_bytes = base64.b64encode(_au_byte_obj)
        _base64_en = _base64_bytes.decode('ascii')
        return _base64_en

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
