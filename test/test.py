def _responseStringToMap(response):
    respValueList = response.split(";")
    valuesMap = {}
    for value in respValueList:       
        valueList = value.split("=")
        valuesMap[valueList[0]] = valueList[1]
    return valuesMap


inputString = input("input: ")
print(_responseStringToMap(inputString))
input("")