# bot.py
import discord
from discord.ext import commands
from urllib.request import urlopen

from bs4 import BeautifulSoup
import grequests
import requests
import time

TOKEN = 'ODI4NDQ0NjMyOTg3MDc0NTgw.YGprMA.UexRcmepOOQo4672UXRXtMQ4BDE'
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True) ###turn on all intents in the bot dashboard

client = commands.Bot(command_prefix=['bf!', 'Bf!', 'bF!', 'BF!', 'bffsie!'], intents=intents)

# for the soup
def fixText(text):
    if text.find("(") != -1:
        return text[0:text.find("(")]
    return text
def clearEmpty(array):
    fixedArray = []
    stringArray = []
    for x in range(len(array)):
        if array[x].get_text() != "":
            if array[x].get_text() not in stringArray:
                stringArray.append(array[x].get_text())
                fixedArray.append(array[x])
    return fixedArray
def getEvents(Events):
    eventObj = []
    for x in range(len(Events)):
        #print(Events[x].find("strong").get_text())
        if(len(clearEmpty(Events[x].find_all("strong"))) > 0):
            event = clearEmpty(Events[x].find_all("strong"))[0].get_text()
            eventObj.append(fixText(event))
            dateB = clearEmpty(Events[x].find_all("b"))
            dateStrong = clearEmpty(Events[x].find_all("strong"))
            if(len(dateStrong) < 2):
                if(dateB):
                    eventObj.append(dateB[0].get_text())
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
    await client.get_channel(736733844958478389).send('hopping in!')

# im keeping this
@client.command()
async def ping(ctx):
    await ctx.reply("pong!")

@client.command()
async def yeehaw(ctx):
    await ctx.reply("cowboys!")

# gets comp dates
@client.command(aliases=['comp', 'dates', 'date', 'comp dates', 'competition', 'competition dates'])
async def comps(ctx, *args):
    # remake the soup, set up for url
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

@client.command(aliases=['pt', 'packet tracer', 'mods', 'h*ll'])
async def cisco(ctx, *args):

    #stolen
    url = "https://www.uscyberpatriot.org/competition/current-competition/challenges-by-round"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("tbody")[1].find_all("strong")


    #tablebody = soup.find(lambda tag: tag.name=='tbody')[1] 

    trainEvents = tablebody.find_all("tr")
    eventObj = getEvents(trainEvents)

    ##or maybe first get bold, search until find modules, return + add to embed

    ##future... search by round
    ##if table data has "modules", add table data to the embed
    ##get round + date somehow...?

    await ctx.send(tablebody)

client.run(TOKEN)
