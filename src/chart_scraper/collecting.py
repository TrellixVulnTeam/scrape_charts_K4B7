from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

class ScrapeCharts:
    """
        Please note: each website should remain in string format
        This class will guide you through the process with print statements
        :String url: list of urls or a single url
        :return: nothing, but a print statement will pop up
        """
    def __init__(self, websites):
        """
        Please note: each website should remain in string format
        """
        self.listedCharts = []
        if websites is str:
            self.websites = [websites]
            print("(scraper) Single website saved as list")
            print(self.websites)
        else:
            self.websites = list(websites)
            print("(scraper) Websites saved as list")
            print(self.websites)
        for eachSite in self.websites:
            self.listedCharts.append(self.getTables(self.scrapeSite(eachSite)))
        print("(scraper) time to choose which charts to keep")
        self.displayTables(self.listedCharts)
        
            
    def scrapeSite(self, url: list):
        """
        Scrape the website (singular) or websites (plural)
        :param url: list of urls or a single url, all urls are in string format
        :return: htmldoc of each item
        """
        toReturn = requests.get(url).content
        print("(scraper) Found" + url)
        return toReturn

    def getTables(self, htmldoc):
        """
        With website or websites, find all tables
        :param htmldoc: list of or one of a htmldoc
        :return: tables as a list
        """
        soup = BeautifulSoup(htmldoc, features="html.parser")
        return self.makelist(soup.findAll('table'))

    def makelist(self, table):
        """
        Print all tables so that you can pick the tables you want (not my code, but still reliable)
        :param listOfTables: list of or one of a htmldoc
        :return: tables as pandas' DataFrame
        """
        result = []
        allrows = table.findAll('tr')
        for row in allrows:
            result.append([])
            allcols = row.findAll('td')
        for col in allcols:
            thestrings = [str(s) for s in col.findAll(text=True)]
            thetext = ''.join(thestrings)
            result[-1].append(thetext)
        return result

    def displayTables(self, listOfTables):
        """
        Print all tables so that you can pick the tables you want
        :param listOfTables: list of or one of a htmldoc
        :return: tables as pandas' DataFrame
        """
        df = pd.DataFrame(listOfTables)
        print(df)
        print("(scraper) Remove unnecsary charts through removing items from the list Scraper.listedCharts")
        print("(scraper) Once done, call Scraper.cleanList with your preferred arguments to preview cleaning")
        return df

    def cleanList(self, whereToSplit=["\(", ","], whereToCombine=["/"], whichToKeep="[a-zA-Z]", whereToClean=[["[^a-zA-Z ]+", ""], [" +", " "]]):
        """
        This functions cleans the list by splitting it and removing unnecessary characters or whitespace
        :list rawList: this is the list that is going to be cleaned
        :param whereToSplit: this is the first part of a regex split function
        :param whereToCombine: this is the first part of a regex split function
        :string whichToKeep: if a regex search function comes up true with this string, then the string is kept, else it's removed
        :List<List<String0, String1> whereToCombine: string0 is first part of regex sub equation, string1 is what is substituted for string0
        :return: processedList
        """
        processedList = []
        for dirtyPart in self.listedCharts:
            # For stepOne, each string is split into parts
            stepOne = []
            for unsplitPart in dirtyPart:
                for splitPoint in whereToSplit:
                    if (re.search(splitPoint, unsplitPart)):
                        splitPart = re.split(splitPoint, unsplitPart)
                        stepOne.append(splitPart)
                    else:
                        stepOne.append([unsplitPart])
            # For stepTwo, each string is combined based on a certain part, eg. this string "a/b/c" is turned into ["a", "ab", "ac"]
            stepTwo = []
            for combinePoint in whereToCombine:
                for listOfUncombinedStrings in stepOne:
                    listOfCombinedParts = []
                    for uncombinedPart in listOfUncombinedStrings:
                        if (re.search(combinePoint, uncombinedPart)):
                            combinedPart = re.split(combinePoint, uncombinedPart)
                            setup = [combinedPart[0]]
                            combinedPart.pop(0)
                            for eachSubPart in uncombinedPart:
                                eachSubPart = setup[0] + eachSubPart
                                setup.append(eachSubPart)
                            combinedPart = setup
                        listOfCombinedParts.append(combinedPart)
                    stepTwo.append(listOfCombinedParts)
            # For stepThree, all empty parts are removed
            stepThree = []
            for listOfUncleanedParts in stepTwo:
                listOfCleanedParts = []
                for uncleanedPart in listOfUncleanedParts:
                    if (bool(re.search(whichToKeep, uncleanedPart))):
                        for cleanPoint in whereToClean:
                            cleanedPart = re.sub(cleanPoint[0], cleanPoint[1], unsplitPart)
                            cleanedPart = unsplitPart.strip()
                            listOfCleanedParts.append(cleanedPart)
                if (listOfCleanedParts):
                    stepThree.append(list(set(listOfCleanedParts)))
            # The last thing to check
            if (stepThree):
                processedList.append(list(set(stepThree)))
        self.listedCharts = processedList
        self.displayTables()
        print("(scraper) Many prefer to turn this list into a dictionary")
        print("(scraper) If you would like this, call scraper.listToDict")
    
    def listToDict(self):
        z = {}
        for eachrow in self.listedCharts:
            try:
                # The index may change for the examples, but usually it's either 2 or 3
                word = eachrow[0]
                definition = eachrow[1]
                examples = eachrow[2]
                for eachword in word:
                    processedExamples = []
                    for eachexample in examples:
                        if eachword in eachexample:
                            processedExamples.append(eachexample) 
                    z.update({eachword: [definition, processedExamples]})
            except IndexError:
                pass
        return z