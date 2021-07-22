from src.chart_scraper.ChartScraper import Scraper
# Importing from pip can be done without the src

# This is for educational purposes only, the fact that there is no assert statements support this idea
if __name__ == "__main__":
    chartScraper = Scraper("https://www.learnthat.org/pages/view/roots.html")
    chartScraper.cleanList()
    chartScraper.listToDict(indexList=[0,1,3])
    chartScraper.getDictKeys()
    chartScraper.displayTables(dataFrame=False)
    print(chartScraper.findWordComponents("Philology"))