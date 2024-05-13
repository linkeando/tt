from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from src.application.utils.constants import Web
import time

class ScrapingAdapter:
    def __init__(self):
        # Inicialización del navegador
        self.driver = webdriver.Chrome()

    def scrape_curp(self, curp):
        # Abrir la página web
        self.driver.get(Web.CURP_URL)

        # Esperar hasta que el campo de entrada de la CURP esté listo
        curp_input = WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "curpinput")))

        # Introducir el CURP en el campo de entrada
        curp_input.send_keys(curp)

        # Verificar si el campo de entrada está lleno
        if curp_input.get_attribute("value"):
            # Esperar hasta que el botón de búsqueda esté listo
            search_button = WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "searchButton")))

            time.sleep(5)  # Esperar 2 segundos (puedes ajustar este valor según sea necesario)

            # Hacer clic en el botón de búsqueda
            search_button.click()

            # Esperar un breve momento antes de hacer clic en el botón de descarga
            time.sleep(5)  # Esperar 2 segundos (puedes ajustar este valor según sea necesario)

            # Hacer clic en el botón de descarga
            download_button = WebDriverWait(self.driver, 10).until(presence_of_element_located((By.ID, "download")))
            download_button.click()

            return "La descarga ha comenzado. Por favor, espera unos momentos."
        else:
            return "Por favor, introduce un CURP válido antes de iniciar la descarga."
