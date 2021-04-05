# bot.py
import discord
from discord.ext import commands
from urllib.request import urlopen

from bs4 import BeautifulSoup
import grequests
import requests
import time

TOKEN = 'ODI4MzEzNTcyODUyNDk4NDUy.YGnxIQ.glzmYv3KgWJeYlizZMASQi2fuQs' #our beautiful token
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True) #yas intents
client = commands.Bot(command_prefix=['bf!', 'Bf!', 'bF!', 'BF!'], intents=intents) #the command is bf![put command here]

# for the soup
def fixText(text): #fixes text for example, round 1(all teams participate), will be changed to just round 1
    if text.find("(") != -1:
        return text[0:text.find("(")]
    return text
def clearEmpty(array): #clears the empty or strings with "" inside of the array so that the algorithms later will work properly.
    fixedArray = [] #sets up the array that we will put the values that are not empty into
    stringArray = [] #sets up the string array that will be compared to the original array so that repeats will not be counted again
    for x in range(len(array)):
        if array[x].get_text() != "": #test if not empty
            if array[x].get_text() not in stringArray: #test if the string isn't already in stringArray. no repeats allowed.
                stringArray.append(array[x].get_text())
                fixedArray.append(array[x])
    return fixedArray
def getEvents(Events): #the real juicy part
    eventObj = [] #sets up the eventObj array to hold the finished eventss
    for x in range(len(Events)):
        #print(Events[x].find("strong").get_text())
        if(len(clearEmpty(Events[x].find_all("strong"))) > 0): #the array should have more than one item, otherwise it doesn't exist and the program will skip it
            event = clearEmpty(Events[x].find_all("strong"))[0].get_text() #gets the event name, because a row will have for example ["Exhibition Round I", "August 7-9, 2020"]
            eventObj.append(fixText(event)) #puts the fixed event name into the eventObj
            dateBold = clearEmpty(Events[x].find_all("b")) #gets values in text elements such as <b>, because cyberpatriot website is wack and one value is in <b> instead of <strong>
            dateStrong = clearEmpty(Events[x].find_all("strong")) #gets all values in text elements of <strong>, will be using it for date, because after the array is cleaned up the date will be the second value
            if(len(dateStrong) < 2): #if for some reason the values in dateStrong is only ["Exhibition Round I"] and doesn't include the date
                if(dateBold): #if dateBold does exist, then we shall use it instead
                    eventObj.append(dateBold[0].get_text()) #puts the first dateBold value into the array
                else:
                    eventObj.append("not found")
            else:
                #print(dateStrong[1].get_text())
                eventObj.append(dateStrong[1].get_text())#puts the second value of dateStrong into the array
    return eventObj

# bot starts
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.get_channel(828314284441337889).send('I am alive') #we've connected to DISCORD!!!!

# im keeping this
@client.command() #the command async functions work like this, async def ping(ctx, *args) would be the command bf!ping on the server with arguments, however, ping doesn't have extra arguments
async def ping(ctx): 
    await ctx.reply("pong!") #always gotta keep the pong

# gets comp dates
@client.command(aliases=['comp'])
async def comps(ctx, *args): #arguments work like page 1 or page 2, bf!comps 1 or bf!comps 2S
    # remake the soup, just gets the website
    url = "https://www.uscyberpatriot.org/competition/current-competition/competition-schedule"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("tbody")#gets all table elements inside of the website, basically the trainingrounds and competitive rounds

    # get args length
    if not args:
        page_num = 1
    else:
        if int(args[0]) > 2 or int(args[0]) < 1: #basically if the value is one or less, then it's just page 1, if it's bigger than one, then it's the value they put in.
            page_num = 1
        else:
            page_num = int(args[0])

    # make the embed or basically what the bot displays
    competition_embed = discord.Embed(
        title=f"Competition Dates:"
    )
    competition_embed.set_thumbnail(url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png") #puts in the picture
    competition_embed.set_footer(text=f"Viewing page {page_num} of 2.") #puts in the page number

    # flavor the soup
    if page_num == 1: # page 1
        trainEvents = tablebody[0].find_all("tr") #table one is the training events
        eventObj = getEvents(trainEvents) #puts the values into the array
        #the next two lines of code bassically skips the first value of the table which says ["EVENTS", "DATES] for the actual stuff
        #it then gets every two values ["Exhibition Round I", "some date", "Training Round I", "some date"], so it would get 0 and 1, then 1 and 2, and put it onto the message
        for x in range(1, int(len(eventObj)/2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False) 
    else: # page 2
        roundEvents = tablebody[1].find_all("tr") #table two on the website is competitive rounds
        eventObj = getEvents(roundEvents)
        for x in range(int(len(eventObj)/2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False)

    # send the soup
    await ctx.send(embed=competition_embed)

client.run(TOKEN)
