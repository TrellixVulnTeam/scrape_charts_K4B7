import re
import pandas as pd
import requests
from requests.api import head

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
        self.dataFrames = []
        if type(websites) is str:
            self.websites = [websites]
            print("(scraper) Single website saved as list")
            print(self.websites)
        else:
            self.websites = websites
            print("(scraper) Websites saved as list")
            print(self.websites)
        for eachSite in self.websites:
            sitesDataFrames = pd.read_html(self.scrapeSite(eachSite))
            self.dataFrames = self.dataFrames + [dataFrame for dataFrame in sitesDataFrames]
        self.displayTables()

    def scrapeSite(self, url):
        """
        Scrape the website (singular) or websites (plural)
        :param url: list of urls or a single url, all urls are in string format
        :return: htmldoc of each item
        """
        toReturn = requests.get(url).text
        print("(scraper) Found " + url)
        return toReturn

    def displayTables(self, dataFrame=True):
        """
        Print all tables so that you can pick the tables you want
        :bool dataFrame: prints the listedChart instead of the dataFrames
        :return: tables as pandas' DataFrame
        """
        if dataFrame:
            print("(scraper) Time to choose which charts to keep, you can only choose one, it'll keep the last one you picked")
            indexToKeep = 0
            for index, eachDataframe in enumerate(self.dataFrames):
                print(eachDataframe)
                keep = input("(scraper) type Keep to keep this dataframe: ")
                if (keep == "Keep"):
                    indexToKeep = index
            self.dataFrames = self.dataFrames[indexToKeep]
        else:
            print(self.listedChart)

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
        for dirtyPart in self.dataFrames.values.tolist():
            # For stepOne, each string is split into parts
            stepOne = []
            for unsplitPart in dirtyPart:
                if type(unsplitPart) is str:
                    for splitPoint in whereToSplit:
                        if (bool(re.search(splitPoint, unsplitPart))):
                            splitPart = re.split(splitPoint, unsplitPart)
                            stepOne.append(splitPart)
                        else:
                            stepOne.append([unsplitPart])
            # For stepTwo, each string is combined based on a certain part, eg. this string 'a/b/c' is turned into ['a', 'ab', 'ac']
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
                            listOfCombinedParts = listOfCombinedParts + setup
                        else:
                            listOfCombinedParts = listOfCombinedParts + [uncombinedPart]
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
                    stepThree.append(tuple(list(set(listOfCleanedParts))))
            # The last thing to check
            if (stepThree):
                processedList.append(tuple(list(set(stepThree))))
        self.listedChart = processedList

    def listToDict(self, indexList=[0, 1, 2], keyAsList=False, includePrintStatement=True):
        """
        This functions converts the saved class variable of the list into a dictionary with the first index as the key and the other indexes in a list. You can change the order by passing in a value for the default.
        :list indexList: this is the order of the indexes used
        :bool keyAsList: should this function convert the key from a list into a single element
        :bool includePrintStatement: prints out "(scraper) You can now get the keys of this dictionary by calling Scraper.getDictKeys()"
        :return: dictionary
        """
        self.dictionariedChart = dict()
        for eachRow in self.listedChart:
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