from src.chart_scraper.ChartScraper import Scraper
# Importing from pip can be done without the src

# This is for educational purposes only, this code is example code, but not for usage
chartScraper = Scraper("https://www.learnthat.org/pages/view/roots.html", chartNumber=[2])
chartScraper.cleanList(whichToKeep="[a-zA-Z0-9 ]+", whereToSplit="\(|,", whereToCombine="/", whereToClean=[[" -", ":"],[";", ","], ["[^a-zA-Z ,:]+", ""], [" +", " "]])
chartScraper.listToDict(includePrintStatement=False)
chartScraper.getDictKeys(includePrintStatement=False)
# All lowercase
chartScraper.findWordComponents("philology")
chartScraper.createDataFrame()
chartScraper.saveFiles(fileType=2)