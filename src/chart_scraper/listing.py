import json


data = {}
with open("combinedData.json", "r") as f:
    data = dict(json.load(f))
listOfKeys = list(data.keys())
print(listOfKeys, len(listOfKeys))
with open("combinedDataList.json", "w") as f:
    json.dump(listOfKeys, f)