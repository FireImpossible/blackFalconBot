# bot.py
import discord
from discord.ext import commands
from urllib.request import urlopen

from bs4 import BeautifulSoup
import grequests
import requests
import time

TOKEN = 'ODI4MzEzNTcyODUyNDk4NDUy.YGnxIQ.glzmYv3KgWJeYlizZMASQi2fuQs'
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=['bf!', 'Bf!', 'bF!', 'BF!'], intents=intents)

# make the soup
url = "https://www.uscyberpatriot.org/competition/current-competition/competition-schedule"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

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

    if not args:
        page_num = 1
    else:
        if int(args[0]) > 2 or int(args[0]) < 1:
            page_num = 1
        else:
            page_num = int(args[0])

    competition_embed = discord.Embed(
        title=f"Competition Dates:"
    )
    competition_embed.set_thumbnail(url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png")
    competition_embed.set_footer(text=f"Viewing page {page_num} of 2.")

    if page_num == 1: # page 1
        for x in range(3):
            mydivs = soup.find_all("tr", {"class": "ms-rteTableOddRow-default"})
            mystrong = mydivs[x].find_all("strong")
            competition_embed.add_field(name=mystrong[0].get_text(), value=mystrong[-1].get_text(), inline=False)

            if x == 0:
                mydivs = soup.find_all("tr", {"class": "ms-rteTableEvenRow-default"})
                mystrong = mydivs[1].find_all("strong")
                competition_embed.add_field(name=mystrong[0].get_text(), value=mystrong[1].get_text(), inline=False)
            elif x == 1:
                mydivs = soup.find_all("tr", {"class": "ms-rteTableEvenRow-default"})
                mystrong = mydivs[2].find_all("strong")
                mybold = mydivs[2].find_all("b")
                competition_embed.add_field(name=mystrong[0].get_text(), value=mybold[0].get_text(), inline=False)
            elif x == 2:
                mydivs = soup.find_all("tr", {"class": "ms-rteTableFooterRow-default"})
                mystrong = mydivs[0].find_all("strong")
                competition_embed.add_field(name=mystrong[0].get_text(), value=mystrong[-1].get_text(), inline=False)
    else: # page 2
        for x in range(3, 5):
            mydivs = soup.find_all("tr", {"class": "ms-rteTableOddRow-default"})
            mystrong = mydivs[x].find_all("strong")
            competition_embed.add_field(name=mystrong[0].get_text()[:7], value=mystrong[1].get_text(), inline=False)

            if x == 3:
                mydivs = soup.find_all("tr", {"class": "ms-rteTableEvenRow-default"})
                mystrong = mydivs[x + 1].find_all("strong")
                competition_embed.add_field(name=mystrong[0].get_text()[:7], value=mystrong[1].get_text(), inline=False)
            else:
                mydivs = soup.find_all("tr", {"class": "ms-rteTableFooterRow-default"})
                mystrong = mydivs[1].find_all("strong")
                competition_embed.add_field(name=mystrong[0].get_text(), value=mystrong[1].get_text(), inline=False)

    await ctx.send(embed=competition_embed)

client.run(TOKEN)
