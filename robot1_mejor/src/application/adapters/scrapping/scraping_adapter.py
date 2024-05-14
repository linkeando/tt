from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.application.utils.constants import Web
from src.application.adapters.scrapping.browser import BrowserDriver


class ScrapingAdapter:
    def __init__(self):
        self.driver = BrowserDriver.init_driver()
        BrowserDriver.set_headers(self.driver)

    def _wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def _input_curp(self, curp):
        curp_input = self._wait_for_element(By.ID, "curpinput")
        curp_input.send_keys(curp)
        return curp_input.get_attribute("value")

    def _click_button(self, by, value, timeout=10):
        button = self._wait_for_element(by, value, timeout)
        button.click()

    def scrape_curp(self, curp):
        self.driver.get(Web.CURP_URL)

        if self._input_curp(curp):
            self._click_button(By.ID, "searchButton")
            self._click_button(By.ID, "download", timeout=5)
            return "La descarga ha comenzado. Por favor, espera unos momentos."
        else:
            return "Por favor, introduce un CURP válido antes de iniciar la descarga."

    def close(self):
        self.driver.quit()
