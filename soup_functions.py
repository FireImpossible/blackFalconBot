from urllib.request import urlopen
from bs4 import BeautifulSoup
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
def getScore(ID):
    url = "http://scoreboard.uscyberpatriot.org/team.php?team=" + ID
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("table")
    tableRows = tablebody[0].find_all("tr")
    headers = tableRows[0].find_all("td")
    correVals = tableRows[1].find_all("td")
    imagetable = tablebody[1]
    images = imagetable.find_all("tr")
    scoreDict = {}
    for x in range(len(headers)):
        scoreDict[headers[x].getText()] = correVals[x].getText()
    def getT(vari):
        return str(vari.getText().lower())
    imagesScoreIndex = images[0].find_all("td")
    imagesScore = map(getT, imagesScoreIndex)
    indexv = list(imagesScore).index("score")
    for x in range(len(images) - 1):
        imageData = images[x + 1].find_all("td")
        scoreDict[imageData[0].getText()] = imageData[indexv].getText()
        print(imageData[-1].getText())
    return scoreDict
    
