import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import DOWNLOAD_DIR
from pages.home_page import HomePage
from utils.file_utils import clean_directory


@pytest.fixture(autouse=True)
def clean_downloads():
    clean_directory(DOWNLOAD_DIR)

    yield

    clean_directory(DOWNLOAD_DIR)


@pytest.fixture
def driver():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()

    prefs = {
        "download.default_directory": str(DOWNLOAD_DIR),
        "download.prompt_for_download": False,
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture
def home_page(driver):
    return HomePage(driver)