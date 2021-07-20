import pprint
import json


data = []
processedData = {}
for i in range(0,3):
    with open("data" + str(i) + ".json") as f:
        data.append(json.load(f))
for eachdict in data:
    for key, value in eachdict.items():
        try:
            valuestocombine = processedData[key]
            valuestocombine[0] = valuestocombine[0] + value[0]
            valuestocombine[0] = list(set(valuestocombine[0]))
            valuestocombine[1] = valuestocombine[1] + value[1]
            valuestocombine[1] = list(set(valuestocombine[1]))
            processedData[key] = valuestocombine
        except KeyError:
            value[0] = list(set(value[0]))
            value[1] = list(set(value[1]))
            processedData[key] = value



pp = pprint.PrettyPrinter(depth=3)
pp.pprint(processedData)


with open("combinedData.json", "w") as f:
    json.dump(processedData, f, indent=4)