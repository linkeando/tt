from src.application.adapters.scrapping.scraping_adapter import ScrapingAdapter


class ScrapingService:
    def __init__(self):
        self.scraping_adapter = ScrapingAdapter()

    def get_curp_data(self, curp):
        curp_data = self.scraping_adapter.scrape_curp(curp)
        return curp_data
