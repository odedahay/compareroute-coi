from splinter import Browser
import unittest

from faker import Faker
fake = Faker()

def login_as_user(browser):
    url = "http://compare-route-3.appspot.com/login"
    browser.visit(url)
    browser.find_by_id('email_user').first.fill("odedahay@gmail.com")
    browser.find_by_id('password_user').first.fill('Pass')
    button = browser.find_by_id('login-button')
    # # Interact with elements
    button.click()
    return browser

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_login_page_loads(self):

        with Browser('chrome') as browser:
            # Visit URL
            url = "http://compare-route-3.appspot.com"
            browser.visit(url)

            links_found = browser.find_link_by_partial_text('Sign in')

            self.assertEquals(len(links_found), 1)

    def test_login_page_logins(self):

        with Browser('chrome') as browser:
            # Visit URL
            url = "http://compare-route-3.appspot.com/login"
            browser.visit(url)
            browser.find_by_id('email_user').first.fill(fake.email())
            #browser.find_by_id('password_user').first.fill('simon_lau@rp.edu.sg')
            browser.find_by_id('password_user').first.fill('odedahay@gmail.com')

            button = browser.find_by_id('login-button')
            # # Interact with elements
            button.click()

            self.assertTrue(browser.is_text_present('Login failed'))

    def test_compare_page(self):
        with Browser('chrome') as browser:
            login_as_user(browser)




if __name__ == '__main__':
    unittest.main()