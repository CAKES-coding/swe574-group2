from needle.cases import NeedleTestCase
from needle.driver import NeedleChrome, NeedleFirefox, NeedleOpera
import time


class AlertTestChrome(NeedleTestCase):

    @classmethod
    def get_web_driver(cls):
        return NeedleChrome()

    def test_masthead(self):
        # All of the functionality of selenium drivers can be used
        self.driver.get('http://34.159.77.79:8000/')
        time.sleep(2)
        self.driver.find_element_by_css_selector('.btn.btn-primary').click()
        time.sleep(2)
        self.assertScreenshot('.alert.alert-danger', 'alert-chrome')


class AlertTestFirefox(NeedleTestCase):

    @classmethod
    def get_web_driver(cls):
        return NeedleFirefox()

    def test_masthead(self):
        self.driver.get('http://34.159.77.79:8000/')
        time.sleep(2)
        self.driver.find_element_by_css_selector('.btn.btn-primary').click()
        time.sleep(2)
        self.assertScreenshot('.alert.alert-danger', 'alert-firefox')


class AlertTestOpera(NeedleTestCase):

    @classmethod
    def get_web_driver(cls):
        return NeedleOpera()

    def test_masthead(self):
        self.driver.get('http://34.159.77.79:8000/')
        time.sleep(2)
        self.driver.find_element_by_css_selector('.btn.btn-primary').click()
        time.sleep(2)
        self.assertScreenshot('.alert.alert-danger', 'alert-opera')
