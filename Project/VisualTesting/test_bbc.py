from needle.cases import NeedleTestCase
from needle.driver import NeedleChrome, NeedleFirefox, NeedleOpera


class NavbarTestChrome(NeedleTestCase):

    @classmethod
    def get_web_driver(cls):
        return NeedleChrome()

    def test_masthead(self):
        self.driver.get('http://34.159.77.79:8000/')
        self.assertScreenshot('nav.navbar', 'navbar-chrome')


class NavbarTestFirefox(NeedleTestCase):

    @classmethod
    def get_web_driver(cls):
        return NeedleFirefox()

    def test_masthead(self):
        self.driver.get('http://34.159.77.79:8000/')
        self.assertScreenshot('nav.navbar', 'navbar-firefox')


class NavbarTestOpera(NeedleTestCase):

    @classmethod
    def get_web_driver(cls):
        return NeedleOpera()

    def test_masthead(self):
        self.driver.get('http://34.159.77.79:8000/')
        self.assertScreenshot('nav.navbar', 'navbar-opera')
