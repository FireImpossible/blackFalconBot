# for the soup
def fixText(text):
    if text.find("(") != -1:
        return text[0:text.find("(")]
    return text
def clearEmpty(array):
    fixedArray = []
    #stringArray = []
    for x in range(len(array)):
        if array[x].get_text() != "":
            if array[x].get_text() not in fixedArray:
                #stringArray.append(array[x].get_text())
                fixedArray.append(array[x].get_text())
    return fixedArray
def getEvents(Events):
    eventObj = []
    for x in range(len(Events)):
        #print(Events[x].find("strong").get_text())
        if(len(clearEmpty(Events[x].find_all("strong"))) > 0):
            event = clearEmpty(Events[x].find_all("strong"))[0]
            eventObj.append(fixText(event))
            dateBold = clearEmpty(Events[x].find_all("b"))
            dateStrong = clearEmpty(Events[x].find_all("strong"))
            if(len(dateStrong) < 2):
                if(dateBold):
                    eventObj.append(dateBold[0])
                else:
                    eventObj.append("not found")
            else:
                #print(dateStrong[1].get_text())
                eventObj.append(dateStrong[1])
    return eventObj