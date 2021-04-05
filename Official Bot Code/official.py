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
            if array[x].get_text() not in stringArray: #test if the string isn't already in stringArray
                stringArray.append(array[x].get_text())
                fixedArray.append(array[x])
    return fixedArray
def getEvents(Events): #the real juicy part
    eventObj = []
    for x in range(len(Events)):
        #print(Events[x].find("strong").get_text())
        if(len(clearEmpty(Events[x].find_all("strong"))) > 0):
            event = clearEmpty(Events[x].find_all("strong"))[0].get_text()
            eventObj.append(fixText(event))
            dateBold = clearEmpty(Events[x].find_all("b"))
            dateStrong = clearEmpty(Events[x].find_all("strong"))
            if(len(dateStrong) < 2):
                if(dateBold):
                    eventObj.append(dateBold[0].get_text())
                else:
                    eventObj.append("not found")
            else:
                #print(dateStrong[1].get_text())
                eventObj.append(dateStrong[1].get_text())
    return eventObj

# bot starts
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.get_channel(828314284441337889).send('I am alive')

# im keeping this
@client.command()
async def ping(ctx):
    await ctx.reply("pong!")

# gets comp dates
@client.command(aliases=['comp'])
async def comps(ctx, *args):
    # remake the soup
    url = "https://www.uscyberpatriot.org/competition/current-competition/competition-schedule"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("tbody")

    # get args length
    if not args:
        page_num = 1
    else:
        if int(args[0]) > 2 or int(args[0]) < 1:
            page_num = 1
        else:
            page_num = int(args[0])

    # make the embed
    competition_embed = discord.Embed(
        title=f"Competition Dates:"
    )
    competition_embed.set_thumbnail(url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png")
    competition_embed.set_footer(text=f"Viewing page {page_num} of 2.")

    # flavor the soup
    if page_num == 1: # page 1
        trainEvents = tablebody[0].find_all("tr")
        eventObj = getEvents(trainEvents)
        for x in range(1, int(len(eventObj)/2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False)
    else: # page 2
        roundEvents = tablebody[1].find_all("tr")
        eventObj = getEvents(roundEvents)
        for x in range(int(len(eventObj)/2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False)

    # send the soup
    await ctx.send(embed=competition_embed)

client.run(TOKEN)
