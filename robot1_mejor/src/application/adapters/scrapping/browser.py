import undetected_chromedriver as uc


class BrowserDriver:
    @staticmethod
    def init_driver():
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--headless')
        driver = uc.Chrome(options=chrome_options)
        return driver

    @staticmethod
    def set_headers(driver):
        driver.execute_cdp_cmd(
            'Network.setUserAgentOverride', {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
            })
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
