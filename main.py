import os
from bot import *
from urllib.request import urlopen

from bs4 import BeautifulSoup
import grequests
import requests 
import time
from soup_functions import * #look i can write tho
from database import *
from badWords import bad_words
from magicBall import *
from manage_timezones import *
import psycopg2
import datetime
import asyncio

import random
import datetime

#time_zone = 4
#remove the time zone difference and implement convertDateTime()

# im keeping this
@client.command()
async def ping(ctx):
    await ctx.reply("pong!")
    if ctx.message.author.has_role("Leadership"):
        await ctx.reply("AHHHHHH")

@client.command()
async def yeehaw(ctx):
    await ctx.reply("cowbois \🤠")


client.run(TOKEN)
