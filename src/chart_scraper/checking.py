import json
import pprint

def findWordComponents(testWord, filepath, printing=True):
    data = {}
    with open(filepath, "r") as f:
        data = dict(json.load(f))
    wordComponents = data.keys()
    foundWordComponents = [eachComponent for eachComponent in wordComponents if eachComponent in testWord]
    foundData = {}
    for eachComponent in foundWordComponents:
        foundData[eachComponent] = data[eachComponent]
    if printing:
        print("You're word was" + testWord)
        pp = pprint.PrettyPrinter(depth=3)
        pp.pprint(foundData)
    return foundData

