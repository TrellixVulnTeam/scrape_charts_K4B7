import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

class Scraper:
    """
        Please note: each website should remain in string format
        This class will guide you through the process with print statements
        :String url: list of urls or a single url
        :return: nothing, but a print statement will pop up
        """
    def __init__(self, websites, chartNumber=[]):
        """
        Please note: each website should remain in string format
        """
        self.listedCharts = list()
        if type(websites) is str:
            self.websites = [websites]
            print("(scraper) Single website saved")
        else:
            self.websites = websites
            print("(scraper) Websites saved")
        for eachSite in self.websites:
            self.listedCharts = self.listedCharts + self.getTables(self.scrapeSite(eachSite))
        self.displayTables(chartNumber=chartNumber)

    def scrapeSite(self, url):
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
        soup = BeautifulSoup(htmldoc, features="html.parser")
        toReturn = []
        for eachTable in soup.findAll("table"):
            toReturn.append(self.makelist(eachTable))
        return toReturn

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

    def displayTables(self, chooseTables=True, displayRawCharts=False, chartNumber=[]):
        """
        Print all tables so that you can pick the tables you want
        :bool chooseTables: chooseTables or display tables
        :bool displayRawCharts: displayRawTables or display the processed combinedChart (works only whenChooseTable is false)
        :bool chartNumber: if you know the indexes of the charts you want
        :return: tables as pandas' DataFrame
        """
        if chooseTables:
            if (not bool(chartNumber)):
                print("(scraper) Time to choose which charts to keep, call this again if you want to remove another chart")
                indexesToKeep = []
                for index, eachDataframe in enumerate(self.listedCharts):
                    print(eachDataframe)
                    keep = input("(scraper) type Keep to keep this dataframe: ")
                    if (keep == "Keep"):
                        indexesToKeep.append(index)
                listsToKeep = list()
                self.combinedChart = []
                if len(indexesToKeep) >= 1:
                    for eachIndex in indexesToKeep:
                        listsToKeep = listsToKeep + self.listedCharts[eachIndex]
                        self.combinedChart = listsToKeep
                else:
                    print("(scraper) No charts chosen, so no lists removed")
            else:
                listsToKeep = list()
                for eachIndex in chartNumber:
                        listsToKeep = listsToKeep + self.listedCharts[eachIndex]
                        self.combinedChart = listsToKeep
        else:
            if displayRawCharts:
                for index, eachDataframe in enumerate(self.listedCharts):
                    print(eachDataframe)
                    input("(scraper) Press enter to continue" + str(index) +": ")
            else:
                print(self.combinedChart)

    def cleanList(self, whichToKeep=False, whereToSplit=False, whereToCombine=False, whereToClean=[]):
        """
        This functions cleans the list by splitting it and removing unnecessary characters or whitespace
        :list rawList: this is the list that is going to be cleaned
        :param whereToSplit: this is the first part of a regex split function
        :param whereToCombine: this is the first part of a regex split function
        :string whichToKeep: if a regex search function comes up true with this string, then the string is kept, else it's removed
        :List<List<String0, String1> whereToCombine: string0 is first part of regex sub equation, string1 is what is substituted for string0
        :return: processedList
        """
        processedTable = []
        for dirtyRow in self.combinedChart:
            # For stepZero, remove any strings without charactes a-z, 0-9, A-Z, or a space (" ")
            stepZero = []
            if (whichToKeep):
                for eachString in dirtyRow:
                    try:
                        if (bool(re.search(whichToKeep, eachString))):
                            stepZero.append(eachString)
                    except:
                        continue
            else:
                stepZero=dirtyRow
            # For stepOne, split strings where necessary
            stepOne=[]
            if (whereToSplit):    
                for unsplitString in stepZero:
                    splitString = re.split(whereToSplit, unsplitString)
                    stepOne.append(splitString)
            else:
                stepOne=stepZero
            # For stepTwo, each string is combined based on a certain part, eg. this string 'a/b/c' is turned into ['a', 'ab', 'ac']
            stepTwo = []
            if (whereToCombine):
                for listOfUncombinedStrings in stepOne:
                    listOfCombinedParts = []
                    for uncombinedPart in listOfUncombinedStrings:
                        combinedPart = re.split(whereToCombine, uncombinedPart)
                        setup = [combinedPart[0]]
                        combinedPart.pop(0)
                        for eachSubPart in combinedPart:
                            eachSubPart = setup[0] + eachSubPart
                            setup.append(eachSubPart)
                        listOfCombinedParts = listOfCombinedParts + setup
                    stepTwo.append(listOfCombinedParts)
            else:
                stepTwo = stepOne
            # For stepThree, all empty parts are removed
            stepThree = []
            for listOfUncleanedStrings in stepTwo:
                listOfCleanedStrings = []
                for uncleanedString in listOfUncleanedStrings:
                    cleanedString = uncleanedString
                    for eachCleanPoint in whereToClean:
                        cleanedString = re.sub(eachCleanPoint[0], eachCleanPoint[1], cleanedString)
                    cleanedString = cleanedString.strip()
                    if(cleanedString or cleanedString not in listOfCleanedStrings):
                        listOfCleanedStrings.append(cleanedString)
                listOfCleanedStrings = (listOfCleanedStrings)
                if (listOfCleanedStrings or listOfCleanedStrings not in stepThree):
                    stepThree.append(listOfCleanedStrings)
            # The last thing to check
            if (stepThree):
                processedTable.append((stepThree))
        self.combinedChart = processedTable
        return self.combinedChart
    
    def listToDict(self, indexList=[0,1,2,3], keysAreLists=False, includePrintStatement=True):
        """
        This functions converts the saved class variable of the list into a dictionary with the first index as the key and the other indexes in a list. You can change the order by passing in a value for the default.
        :list indexList: this is the order of the indexes used
        :bool keyAsList: should this function convert the key from a list into a single element
        :bool includePrintStatement: prints out "(scraper) You can now get the keys of this dictionary by calling Scraper.getDictKeys()"
        :return: dictionary
        """
        self.dictionariedChart = dict()
        for eachRow in self.combinedChart:
            try:
                reorderedList = []
                for eachIndex in indexList:
                    reorderedList.append(eachRow[eachIndex])
                key = reorderedList[0]
                reorderedList.pop(0)
                if keysAreLists:
                    self.dictionariedChart.update({key: reorderedList})
                else:
                    for eachKey in key:
                        self.dictionariedChart.update({eachKey: reorderedList})
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
        self.dictKeys = self.dictionariedChart.keys()
        if includePrintStatement:
            print("(scraper) You can get the keys by calling Scraper.dictKeys or saving the return statement")
        return self.dictKeys

    def findWordComponents(self, testWord):
        """
        This functions finds any key in the dictionary that is a component of the testWord. If you don't want a comprehensive search, just do Scraper.
        :param test: usually a string, however, other options will work
        :return: dictionary with keys and values that worked
        """
        foundKey = [eachComponent for eachComponent in self.dictionariedChart if eachComponent in testWord]
        foundData = dict()
        for eachKey in foundKey:
            foundData.update({eachKey: self.dictionariedChart[eachKey]})
        print(foundData)
        return foundData
    
    def createDataFrame(self):
        """
        This functions creates a pandas dataFrame from this class' saved dictionary.
        :return: Pandas dataframe
        """
        self.dataFrame = pd.DataFrame.from_dict(self.dictionariedChart)
        return self.dataFrame
    
    def saveFiles(self, filePath=False, fileType=0):
        """
        This function saves the dataFrame present. Don't put the file format in the filePath
        :string filePath: empty filepath, nothing happens, else assign a filepath without an extension that is either fixed ("eg. C:/Users/yourUserNameHere/Downloads/data") or relative (eg. "data")
        :string fileType: 0 is list, 1 is dictionary, 2 is pandas Dataframe
        :return: the filetype you choose
        """
        if (filePath):
            if fileType == 0:
                with open(filePath + '.txt', 'w') as f:
                    for listitem in self.combinedChart:
                        f.write('%s\n' % listitem)
                return self.combinedChart
            elif fileType == 1:
                with open(filePath + '.txt', 'w') as f:
                    json.dumps(self.dictionariedChart, f, indent=4)
                return self.dictionariedChart
            elif fileType == 2:
                self.dataFrame.to_csv(filePath)
                return self.dataFrame
        else:
            if fileType == 0:
                return self.combinedChart
            elif fileType == 1:
                return self.dictionariedChart
            elif fileType == 2:
                return self.dataFrame