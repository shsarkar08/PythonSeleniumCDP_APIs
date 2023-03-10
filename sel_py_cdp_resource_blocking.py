from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import unittest


class test_network_intercept(unittest.TestCase):

    _url = 'https://www.amazon.in/'
    _amzon_pay_link = (By.XPATH,"//*[@id='nav-xshop']/a[contains(text(),'Amazon Pay')]")
    _amazon_pay_balance = (By.XPATH,"//*[@id='APayBalance']//span[contains(text(),'Pay balance')]")

    def setUp(self):
        self.svc = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.svc)

        #self.prefs = {"profile.managed_default_content_settings.images": 2}
        #self.chrome_options.add_experimental_option("prefs", self.prefs)
        #self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        self.driver.maximize_window()
        '''
        Enable the Network & Pass URL/Resource patterns to block using Chrome Devtools Protocol API
        '''
        self.driver.execute_cdp_cmd('Network.enable',{})
        self.driver.execute_cdp_cmd('Network.setBlockedURLs',self.blocked_resources())

        self.driver.get(self._url)

    def test_faster_page_load(self):

            driver = self.driver
            try:
                driver.find_element(*self._amzon_pay_link).click()

                assert '_apay' in self.driver.current_url
                print('Navigated to Amazon Pay Page: ', driver.current_url)
                WebDriverWait(driver,10).until(EC.visibility_of_element_located(self._amazon_pay_balance))
                driver.save_screenshot('./AmazonPay_Page.png')

            except NoSuchElementException as exep:
                print('Errrrrrr....')
                with open('exep.log',"w+") as err:
                    err.write(str(exep))

    def blocked_resources(self):
        self.resources = {'urls':[
            '*.jpg', '*.png', '*.gif'
        ]}
        return self.resources

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
