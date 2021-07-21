from src.chart_scraper.ChartScraper import Scraper


# This is for educational purposes only, the fact that there is no assert statements support this idea
chartScraper = Scraper("https://www.learnthat.org/pages/view/roots.html")
chartScraper.cleanList()
chartScraper.listToDict(indexList=[0,1,3])
chartScraper.listToDict()
chartScraper.getDictKeys()
print(chartScraper.findWordComponents("Philology"))