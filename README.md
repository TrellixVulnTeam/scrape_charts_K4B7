# Scrape Charts

Follow the steps completed in test_scraper.py (located in the tests folder or below). The virtual environment is not necessary, pip will download all required packagesdoes not need to be activited, but the import statements probably appear slightly differently, however comments will rectify your confusion on the correct string to paste.

Main feature: scrape charts from multiple websites into one large list

Features include:

* Scraping a chart from a website or multiple websites
* Choosing and combining multiple websites' chartsinto one large list
* Processing that larger list into a cleaned list
* Converting that cleaned list into a panda dictionary
* Converting that cleaned list into a dictionary
* Saving those cleaned list into a json file, etc
* A very friendly to use class that does everything for you
* A very friendly to use class that also has return statements at each stage so that if one part doesn't work, you can see the data and process it yourself (a contingency, as if you contacted me, I would fix the issue)
* A maintainer
* No bugs or issues at the time of writing, (unit testing in place, )
* Regex functions that are explained below

```Python
from src.chart_scraper.ChartScraper import Scraper
# Importing from pip can be done without the src

# This is for educational purposes only, this code is example code, but not for usage
chartScraper = Scraper("https://www.learnthat.org/pages/view/roots.html", chartNumber=[2])
# At this stage. chartScraper.combinedCharts hold this one mega list, so you can manually change one or two things, however this isn't necessary, the following code below will still work as if nothing happened
chartScraper.cleanList(whichToKeep="[a-zA-Z0-9 ]+", whereToSplit="\(|,", whereToCombine="/", whereToClean=[[" -", ":"],[";", ","], ["[^a-zA-Z ,:]+", ""], [" +", " "]])
chartScraper.listToDict(includePrintStatement=False)
chartScraper.getDictKeys(includePrintStatement=False)
# All lowercase
chartScraper.findWordComponents("philology")
chartScraper.createDataFrame()
chartScraper.saveFiles(fileType=2)
```

```Python
chartScraper.cleanList(whichToKeep="[a-zA-Z0-9]+", whereToSplit="\(|,", whereToCombine="/", whereToClean=[[" -", ":"],[";", ","], ["[^a-zA-Z ,:]+", ""], [" +", " "]])
# whichToKeep="[a-zA-Z0-9 ]+" removes strings that don't contain either letters (a-z, A-Z) or numbers (0-9, eg. the larger number 123 works)
# whereToSplit="\(|," splits the string whenever there is a parantehsis or comma, the paranthesis is backslashed because regex requires it
# whereToCombine="/" combines a/b/c into ["a", "ab", "ac"], my niche case required it when I built this package
# whereToClean=[[" -", ":"],[";", ","], ["[^a-zA-Z ,:]+", ""], [" +", " "]]
# [" -", ":"] turns any " -" into ":"
# Likewise, [";", ","] converts ";" into ","
# ["[^a-zA-Z ,:]+", ""] removes characters that aren't letters (a-z, A-z), spaces (" "), commas (,), or colons (:)
# [" +", " "] rectifies the issue of multiple spaces into one space, eg "            " into " "
```
