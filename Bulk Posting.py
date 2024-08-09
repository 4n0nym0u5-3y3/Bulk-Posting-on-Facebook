from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import os

class SocialAutomation:
    def __init__(self):
        # Initialize instance variables
        self.home_url = "https://www.facebook.com/"
        self.pages_url = "https://www.facebook.com/pages/?category=your_pages&ref=bookmarks"
        self.driver_path = os.path.abspath("chromedriver.exe")
        self.browser = None
        self.page_visits = 0
        self.is_logged_in = False
        self.wait_time = 5 # seconds
        self.username_xpath = "//input[@id='email']"
        self.password_xpath = "//input[@id='pass']"
        self.username = None
        self.password = None
        self.logout_xpaths = [
            "//*[@id='userNavigationLabel']",
            "//span[text()='Log Out']"
        ]
        self.page_names = None
        self.post_xpaths = [
            "//textarea[@name='xhpc_message']",
            "//button[contains(., 'Post')]"
        ]
        self.post_content = None

    def start_browser(self):
        if not self.browser:
            self.browser = webdriver.Chrome(self.driver_path)
            return True
        return False

    def close_browser(self):
        if self.browser:
            self.browser.quit()
            self.browser = None
            return True
        return False

    def navigate_to(self, url=None):
        if not self.browser:
            return False
        self.browser.get(url or self.home_url)
        self.page_visits += 1
        return True

    def go_back(self, steps=1):
        if not self.page_visits:
            return False
        for _ in range(steps):
            self.browser.back()
            self.page_visits -= 1
        return True

    def login(self, username=None, password=None):
        if not self.browser or self.is_logged_in:
            return False
        self.browser.find_element_by_xpath(self.username_xpath).send_keys(username or self.username)
        self.browser.find_element_by_xpath(self.password_xpath).send_keys(password or self.password, Keys.RETURN)
        self.is_logged_in = True
        return True

    def logout(self):
        if not self.browser or not self.is_logged_in:
            return False
        try:
            self.browser.find_element_by_xpath(self.logout_xpaths[0]).click()
            time.sleep(self.wait_time)
            self.browser.find_element_by_xpath(self.logout_xpaths[1]).click()
            return True
        except Exception as e:
            print(f"Logout failed: {e}")
            return False

    def wait(self, seconds=None):
        time.sleep(seconds or self.wait_time)
        return True

    def navigate_to_page(self, partial_link_text):
        if not self.browser:
            return False
        self.browser.find_element_by_partial_link_text(partial_link_text).click()
        self.page_visits += 1
        return True

    def post_content_on_page(self):
        if not self.browser:
            return False
        try:
            self.browser.find_element_by_xpath(self.post_xpaths[0]).click()
            time.sleep(self.wait_time)
            self.browser.find_element_by_xpath(self.post_xpaths[0]).send_keys(self.post_content)
            time.sleep(self.wait_time)
            self.browser.find_element_by_xpath(self.post_xpaths[1]).click()
            time.sleep(self.wait_time)
            return True
        except Exception as e:
            print(f"Posting failed: {e}")
            return False

    def load_credentials_from_json(self):
        try:
            with open("credentials.json", "r") as file:
                data = json.load(file)
                self.page_names = data["Pages"]
                self.username = data["Username"]
                self.password = data["Password"]
            return True
        except Exception as e:
            print(f"Failed to load credentials: {e}")
            return False

    def load_post_content(self):
        try:
            with open("post_content.txt", "r") as file:
                self.post_content = file.read()
            return True
        except Exception as e:
            print(f"Failed to load post content: {e}")
            return False

def main():
    bot = SocialAutomation()
    bot.start_browser()
    bot.load_credentials_from_json()
    bot.load_post_content()
    bot.navigate_to()
    bot.login()

    input("Press Y after handling any 2FA or notification prompts and you're ready to post...")

    bot.navigate_to(bot.pages_url)
    bot.wait()

    for page in bot.page_names:
        bot.navigate_to_page(page)
        bot.wait()
        bot.post_content_on_page()
        print(f"Posted content on {page}")

    bot.logout()
    bot.close_browser()
    print("Automation task completed!")

if __name__ == "__main__":
    main()
