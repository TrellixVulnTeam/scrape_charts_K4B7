from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

class Scraper:
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
        if type(websites) is str:
            self.websites = [websites]
            print("(scraper) Single website saved as list")
            print(self.websites)
        else:
            self.websites = websites
            print("(scraper) Websites saved as list")
            print(self.websites)
        for eachSite in self.websites:
            self.getTables(self.scrapeSite(eachSite))
        for eachRawChart in self.rawCharts:
            self.listedCharts.append(self.makelist(eachRawChart))
        self.displayTables()
        
            
    def scrapeSite(self, url: list):
        """
        Scrape the website (singular) or websites (plural)
        :param url: list of urls or a single url, all urls are in string format
        :return: htmldoc of each item
        """
        toReturn = requests.get(url).text
        print("(scraper) Found " + url)
        return toReturn

    def getTables(self, htmldoc):
        """
        With website or websites, find all tables
        :param htmldoc: list of or one of a htmldoc
        :return: tables as a list
        """
        soup = BeautifulSoup(htmldoc, features="lxml")
        print("(scraper) BeautifulSoup has parsed the website")
        self.rawCharts = list()
        self.rawCharts = self.rawCharts + soup.find_all('table')

    def makelist(self, table):
        """
        Print all tables so that you can pick the tables you want
        :param listOfTables: list of or one of a htmldoc
        :return: tables as pandas' DataFrame
        """
        com=[]
        for row in table.find_all("tr")[1:]:
            print(row)
            col = row.find_all("td")
            print(col)
            if len(col)> 0:
                temp=col[1].contents[0]
                try:
                    to_append=temp.contents[0]
                except Exception as e:
                    to_append=temp
                com.append(to_append)
        return com

    def displayTables(self):
        """
        Print all tables so that you can pick the tables you want
        :param listOfTables: list of or one of a htmldoc
        :return: tables as pandas' DataFrame
        """
        print("(scraper) Time to choose which charts to keep")
        chartsToKeep = []
        for eachChart in self.listedCharts:
            df = pd.DataFrame(eachChart)
            print("\n" + df + "\n")
            df.to_clipboard()
            keepOrRemove = input("(scraper) Chart also copied to clipboard, type \"Keep\" or \"Remove\" without the quotation mark to keep or remove the chart\n What do you choose: ")
            if (input == "Keep"):
                chartsToKeep.append(eachChart)
            else: 
                pass
        self.listedCharts = chartsToKeep

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
        print("(scraper) If you would like this, call Scraper.listToDict()")
    
    def listToDict(self, indexList=[0, 1, 2], keyAsList=False, includePrintStatement=True):
        """
        This functions converts the saved class variable of the list into a dictionary with the first index as the key and the other indexes in a list. You can change the order by passing in a value for the default.
        :list indexList: this is the order of the indexes used
        :bool keyAsList: should this function convert the key from a list into a single element
        :bool includePrintStatement: prints out "(scraper) You can now get the keys of this dictionary by calling Scraper.getDictKeys()"
        :return: dictionary
        """
        self.dictionariedChart = dict()
        for eachRow in self.listedCharts:
            try:
                reorderedList = []
                for eachIndex in indexList:
                    reorderedList.append(eachRow[eachIndex])
                key = reorderedList[0]
                value = reorderedList.pop(0)
                if keyAsList:
                    self.dictionariedChart.update({key: value})
                else:
                    for eachItem in key:
                        self.dictionariedChart.update({eachItem: value})
            except IndexError:
                pass
        if includePrintStatement:
            print("(scraper) You can now get the keys of this dictionary by calling Scraper.getDictKeys()")
        return self.dictionariedChart
    
    def getDictKeys(self, includePrintStatement=True):
        """
        This functions gets all the keys from the dictionary
        :bool includePrintStatement: prints out "(scraper) You can get the keys by calling Scraper.dictKeys or saving the return statement"
        :return: list of keys
        """
        self.dictKeys = dict(self.dictionariedChart).keys()
        if includePrintStatement:
            print("(scraper) You can get the keys by calling Scraper.dictKeys or saving the return statement")
        return self.dictKeys

    def findWordComponents(self, testWord):
        """
        This functions finds any key in the dictionary that is a component of the testWord. If you don't want a comprehensive search, just do Scraper.
        :param test: usually a string, however, other options will work
        :return: dictionary with keys and values that worked
        """
        components = self.dictKeys
        foundKey = [eachComponent for eachComponent in components if eachComponent in testWord]
        foundData = {}
        for eachKey in foundKey:
            foundData.update({eachKey: components[eachKey]})
        print(foundData)
        return foundData