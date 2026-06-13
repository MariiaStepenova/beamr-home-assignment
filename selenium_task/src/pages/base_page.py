from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT


class BasePage:
    PATH = None

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        if self.PATH is None:
            raise NotImplementedError(f"{self.__class__.__name__} must define PATH")

        self.driver.get(BASE_URL + self.PATH)

    def _wait_for_clickable(self, locator):
        return WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(locator)
        )

    def _wait_for_visible(self, locator):
        return WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(locator)
        )