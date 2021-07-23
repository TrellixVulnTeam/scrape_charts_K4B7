from src.chart_scraper.ChartScraper import Scraper
# Importing from pip can be done without the src

# This is for educational purposes only, there is no assert statements
chartScraper = Scraper("https://www.learnthat.org/pages/view/roots.html")
chartScraper.cleanList()
chartScraper.displayTables(chooseTables=False)
chartScraper.listToDict(indexList=[0,1,3])
chartScraper.getDictKeys()
print(chartScraper.findWordComponents("Philology"))