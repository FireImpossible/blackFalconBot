# bot.py
##wya...
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
import os

import random
import datetime

#time_zone = 4
#remove the time zone difference and implement convertDateTime()
# bot starts
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    #thien's thing:
    for guild in client.guilds:
        print(guild.name)
        text_channel_list = []
        channelname = []
        for channel in guild.channels: #getting all channels in the servers
            print(str(channel.name) + " type: " + str(channel.type)) 
            if str(channel.type).lower() == 'text': #if it's a text channel
                text_channel_list.append(channel) #gets actual channel
                channelname.append(channel.name) #gets channel name
                print(channel.name)
        print(text_channel_list)
        await client.get_channel(LOG_CHANNEL_ID).send("Your Best BF is Online!")
        # await client.get_channel(text_channel_list[channelname.index("bot-spam")].id).send('Your Best BF is Online') #we've connected to DISCORD!!!!
        client.loop.create_task(gm_message())
        
        
@client.event
async def on_message(message):
    if client.user != message.author:
        if message.content.lower() == 'rank':
            await message.author.send('youre not getting to #1 bro \✨')
        for word in bad_words:
            if word in message.content.lower():
                await message.author.send(f'Your message was deleted because it contained "{word}".')
                await client.get_channel(LOG_CHANNEL_ID).send(f"{message.author} decided to be naughty and said a bad word!")
                await message.delete()
                return
    await client.process_commands(message)
    

# help command stuff
client.remove_command("help")
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title = "Help",
        description = "Use bf!help <command> for more information for each command"
    )
    embed.add_field(name="**ping**", value="pong :)")
    embed.add_field(name="**comp**", value="competition dates")
    embed.add_field(name="**cisco**", value="PT modules")
    embed.add_field(name="**yeehaw**", value="cowboy")
    for x in ctx.message.author.roles:
        if "Leadership" in str(x):
            embed.add_field(name="**announce**", value="say something to everyone")
            embed.add_field(name="**schedule**", value="schedule an announcement")
            embed.add_field(name="**quote**", value="if someone says something stupid, save it")
    await ctx.send(embed=embed)
@help.command()
async def ping(ctx):
    embed = discord.Embed(
        title = "Ping",
        description = "Sends back a pong. The first command that this bot did. " + 
                      "\nIt is very important, and will not be deleted."
    )
    embed.add_field(name="**Syntax**", value="bf!ping")
    await ctx.send(embed=embed)
@help.command(aliases=['comp', 'dates', 'date', 'comp_dates', 'competition', 'competition_dates'])
async def comps(ctx):
    embed = discord.Embed(
        title = "Competition Dates",
        description = "Gets all of the training and competition rounds and dates from the CyberPatriot website and displays them."
    )
    embed.add_field(name="**Syntax**", value="bf!comp <page #>")
    embed.add_field(name="**Aliases**", value="comp, comps, dates, date, comp_dates, competition, competition_dates")
    await ctx.send(embed=embed)
@help.command(aliases=['pt', 'packet_tracer', 'mods', 'h*ll'])
async def cisco(ctx):
    embed = discord.Embed(
        title = "Cisco",
        description = "Says all of the packet tracer modules that is covered for each round."
    )
    embed.add_field(name="**Syntax**", value="bf!cisco")
    embed.add_field(name="**Aliases**", value="cisco, pt, packet_tracer, mods, h*ll")
    await ctx.send(embed=embed)
@help.command()
async def yeehaw(ctx):
    embed = discord.Embed(
        title = "Yeehaw",
        description = "Cowboy <:abelpog:824676945639243812>"
    )
    embed.add_field(name="**Syntax**", value="bf!yeehaw")
    await ctx.send(embed=embed)
@help.command()
@commands.has_role("Leadership")
async def announce(ctx):
    embed = discord.Embed(
        title = "Announce",
        description = "Send a message to the random announcement channel"
    )
    embed.add_field(name="**Syntax**", value="bf!announce <message>")
    await ctx.send(embed=embed)
@help.command()
@commands.has_role("Leadership")
async def schedule(ctx):
    embed = discord.Embed(
        title = "Schedule",
        description = "Schedule an announcement to happen at a later time, or date"
    )
    embed.add_field(name="**Syntax**", value="bf!schedule <date> <time> <message>")
    embed.add_field(name="**Date**", value="There always has to be a date, even if you just want to send it later that day.\n" +
                                           "The date has to be in the <MM/DD/YYYY> (you can also just put '21' for the year)", inline=False)
    await ctx.send(embed=embed)
@help.command()
@commands.has_role("Leadership")
async def quote(ctx):
    embed = discord.Embed(
        title = "Quote",
        description = "Save any message anyone sends"
    )
    embed.add_field(name="**Syntax**", value="bf!quote <message-id>")
    embed.add_field(name="**message-id**", value="To get a message's 'message-id', you must be in developer mode and then right click on the message and click 'Copy ID'", inline=False)
    await ctx.send(embed=embed)

# im keeping this
@client.command()
async def ping(ctx):
    await ctx.reply("pong!")
    if ctx.message.author.has_role("Leadership"):
        await ctx.reply("AHHHHHH")

@client.command()
async def yeehaw(ctx):
    await ctx.reply("cowbois \🤠")

@client.command()
@commands.has_role("Leadership")
async def announce(ctx, *args):
    text = ""
    if not args: return
    else: # put the whole thing into a string
        for arg in args:
            text += arg + " "
    
    desired_guild = ctx.guild
    text_channel_list = []
    channelname = []
    for channel in desired_guild.channels: #getting all channels in the servers
        if str(channel.type).lower() == 'text': #if it's a text channel
            text_channel_list.append(channel) #gets actual channel
            channelname.append(channel.name) #gets channel name
    await client.get_channel(text_channel_list[channelname.index("random-announcement-channel")].id).send(f"@everyone \n" + text) #we've connected to DISCORD!!!!

def delete_scheduled(my_id):
    message = "Announcement " + str(my_id) + " has been deleted"
    try: 
        cur.execute("DELETE FROM announcements WHERE id = %s", (my_id,))
    except:
        message = "That message doesn't exist!" 
    return message


@client.command()
@commands.has_role("Leadership")
async def schedule(ctx, *args):
    text = ""
    time_string = ""
    date = []
    time = []
    if not args: return
    elif args[0] == 'show':
        my_page = 1
        try:
            my_page = int(args[1])
        except:
            my_page = 1
        await ctx.send(embed=get_scheduled(ctx.guild, my_page))
        return
    elif args[0] == 'delete':
        delete_id = 0
        try:
            delete_id = int(args[1])
        except:
            delete_id = 0
        await ctx.send(delete_scheduled(delete_id))
    else:
        try:
            date = args[0].split("/")
            time = args[1].split(":")
            if (int(date[2]) < 100): 
                date[2] = int(date[2]) + 2000
            # set time
            if len(time) == 3: # includes seconds
                my_time = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1]), int(time[2]))
            else: # doesn't include seconds
                my_time = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1]))
            # set the text
            for arg in args[2:]:
                text += arg + " "
            time_string = f"{time[0]}:{time[1]} am"
        except:
            exception_embed = discord.Embed(
                title=f"You're fukcing wrong \✨"
            )
            exception_embed.add_field(name="**The** ***CORRECT***  **Syntax**", value="bf!schedule <MM/DD/YYYY> <HH:MM> <announcement>")
            exception_embed.add_field(name="**Year restriction** \✨", value="Has to be from 0-9999, no exceptions.")
            exception_embed.add_field(name="**Month restriction** \✨", value="Has to go 1-12, no exceptions.")
            exception_embed.set_footer(text="Do it right next time.")
            await ctx.send(embed=exception_embed)
            return
    if int(time[0]) == 12: time_string = f"{time[0]}:{time[1]} pm"
    elif int(time[0]) > 12: time_string = f"{(int(time[0]) - 12)}:{time[1]} pm"
    write_time = my_time
    my_time = convertDateTime(my_time)
    today = datetime.datetime.now()
    countdown = my_time - today
    if countdown.total_seconds() < 0: 
        await ctx.send("Your time has already passed, change it to a time in the future")
        return
    # messages
    await ctx.send(f"Scheduled the message for {date[0]}/{date[1]}/{date[2]} at {time_string}")
    await client.get_channel(LOG_CHANNEL_ID).send(f"{ctx.message.author} scheduled the following message for {date[0]}/{date[1]}/{date[2]} at {time_string}:\n**{text}**")
    # put it into the database
    cur.execute("INSERT INTO announcements (datetime, message, guildName) VALUES(%s, %s, %s)", (write_time, text, str(ctx.guild)))
    conn.commit()
    # get the id
    cur.execute("SELECT * FROM announcements")
    s = cur.fetchall()
    message_id = s[-1][0]
    # wait the time
    await asyncio.sleep(countdown.total_seconds())
    # put it in a certain channel lmao
    await message_send(ctx.guild, "getting-rank", text)
    # after sending, remove it from the database
    cur.execute("DELETE FROM announcements WHERE id = %s", (message_id,))
    conn.commit()

def get_scheduled(guild, page):

    cur.execute("SELECT * FROM announcements WHERE guildName = %s", (str(guild),))
    announce = cur.fetchall()

    sched_embed = discord.Embed(
        title=f"Scheduled Announcements:"
    )
    

    max_pages = round(len(announce) / 10)

    if (page > max_pages): page = max_pages
    #competition_embed.set_thumbnail(url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png")
    sched_embed.set_footer(text=f"Viewing page {page + 1} out of {max_pages + 1}.")   

    page_start = (page) * 10
    page_end = page_start + 9

    if(page == max_pages):
        page_end = len(announce)

    for x in range(page_start, page_end):
        announcemented = announce[x]
        my_id = announcemented[0]
        my_date = str(announcemented[1])
        my_message = announcemented[2]

        schedule_shower = my_message + " scheduled for " + my_date
        sched_embed.add_field(name=my_id, value=schedule_shower, inline=False)

    #for announcemented in announce:
        
        
    ##deal with pages later....
    # # get args length
    # if not args:
    #     page_num = 1
    # else:
    #     if int(args[0]) > 2 or int(args[0]) < 1:
    #         page_num = 1
    #     else:
    #         page_num = int(args[0])

    return sched_embed
    
    
# gets comp dates
@client.command(aliases=['comp', 'dates', 'date', 'comp_dates', 'competition', 'competition_dates'])
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

@client.command(aliases=['pt', 'packet_tracer', 'mods', 'h*ll'])
async def cisco(ctx, *args):

    #stolen
    url = "https://www.uscyberpatriot.org/competition/current-competition/challenges-by-round"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("tbody")[1].find_all("tr")

    ##set up some dictionary
    mod_dict = {}
    test_string = ''
    for trCount in range(0, len(tablebody)):
        
        strong = tablebody[trCount].find(lambda tag: tag.name=='td' and "Round" in tag.text)
        
        ##for every <strong> tag that's found
        if strong:
            key = strong.get_text()
            mod_dict[key] = ''
            test_string += '\n' + str(key) #testing 

            ## search trs until next td with strong + round is found
            trMod = trCount + 1
            next_strong = tablebody[trMod].find(lambda tag: tag.name=='td' and "Round" in tag.text)
            
            while not next_strong and trMod < len(tablebody)-1:
            #for trMod in range(trCount + 1, len(tablebody)):

                module = tablebody[trMod].find(lambda tag: tag.name=='td' and "Module" in tag.text)
                ##search until the text in the tr tag has the text "module"
                if module:
                    mod_dict[key] += '\n' +  str(module.get_text())
                    test_string += '\n' +  str(module.get_text())
                    ##add to dictionary
                trMod+=1
                next_strong = tablebody[trMod].find(lambda tag: tag.name=='td' and "Round" in tag.text) #recursion potential
    
    ##for each key in dict... make an embed
    cisco_embed = discord.Embed(
        title=f"cisco mods <3:"
    )
    cisco_embed.set_thumbnail(url="https://www.saashub.com/images/app/service_logos/51/4ef1468caaa3/large.png?1558762812")
    for key in mod_dict.keys():
        cisco_embed.add_field(name=key, value=mod_dict[key], inline=False)

    await ctx.send(embed=cisco_embed)

#@client.event ###how do you do it so its when the bot joins, is it broken in general, why is the ctx underlined
async def gm_message():

    message_hour = 7
    message_minute = 25

    wakey_messages = ['early birdies get the wormies', 'wake up eggies, stretch your leggies', "get up hatchlings or you'll need patchlings", 'come on falcons, make some palcons', 'leave the nest, or youll have nothing left', 'wakey wakey eggs and bakey', 'get out of beddies if youre not deddies', 'time for yall eggies to get cracking', 'wake up late and youre falcon bait', 'rise and shine or they will dine', 'if youre not awake youll be baked', 'sleep is canceled so you dont get scrambled']

    right_now = datetime.datetime.now()# - datetime.timedelta(hours=time_zone) remove this to implement autotimezone
    hour = right_now.hour
    second = right_now.second
    minute = right_now.minute
    day = right_now.day
    month = right_now.day
    time_dif = 0

    if hour == message_hour and minute == message_minute and second == 0:
        time_dif = 0
        return False
    elif hour <= message_hour:
        time_dif = (convertDateTime(datetime.datetime(2021, month, day, message_hour, message_minute, 0)) - datetime.datetime(2021, month, day, hour, minute, second)).total_seconds()
        ##schedule for those secs
    else:
        ##how long has passed since 8 am
        time_dif = (datetime.datetime(2021, month, day, hour, minute, second) - datetime.datetime(2021, month, day, message_hour, message_minute, 0)).total_seconds()
        time_dif = 86400 - time_dif
    
    await asyncio.sleep(time_dif)

    ##randomize a method
    message = wakey_messages[random.randint(0, (len(wakey_messages)-1))]
    
    for guild in client.guilds:
        text_channel_list = []
        channelname = []
        for channel in guild.channels: #getting all channels in the servers
            if str(channel.type).lower() == 'text': #if it's a text channel
                text_channel_list.append(channel) #gets actual channel
                channelname.append(channel.name) #gets channel name
        await client.get_channel(text_channel_list[channelname.index("cargo-hold")].id).send(message) #we've connected to DISCORD!!!!
        
    while True:
        await asyncio.sleep(86400)

        ##randomize a method
        message = wakey_messages[random.randint(0, (len(wakey_messages)-1))]
        
        for guild in client.guilds:
            text_channel_list = []
            channelname = []
            for channel in guild.channels: #getting all channels in the servers
                if str(channel.type).lower() == 'text': #if it's a text channel
                    text_channel_list.append(channel) #gets actual channel
                    channelname.append(channel.name) #gets channel name
            await client.get_channel(text_channel_list[channelname.index("bot-spam")].id).send(message) #we've connected to DISCORD!!!!

async def message_send(guild, row, channel_name, message):
    text_channel_list = []
    channelname = []

    for g in client.guilds:
        if g.name == guild:
            guild = g
    for channel in guild.channels: #getting all channels in the servers
        if str(channel.type).lower() == 'text': #if it's a text channel
            text_channel_list.append(channel) #gets actual channel
            channelname.append(channel.name) #gets channel name
    # check if still send message
    cur.execute("SELECT * FROM announcements")
    s = cur.fetchall()
    for x in s:
        if row in x:
            await client.get_channel(text_channel_list[channelname.index(channel_name)].id).send(message) #we've connected to DISCORD!!!!
            cur.execute("DELETE FROM announcements WHERE id = %s", (row,))
            conn.commit()
            break

##get data...
async def sched_message(row, message, time_dif, guild):
    await asyncio.sleep(float(time_dif))
    await message_send(guild, row, "getting-rank", message)

# schedules all of the announcements when bot reloads
cur.execute("SELECT * FROM announcements")
announce = cur.fetchall()
for announcemented in announce:
    my_date = convertDateTime(announcemented[1])
    seconds = (my_date - datetime.datetime.now()).total_seconds()
    my_id = announcemented[0]
    if seconds > 0:
        my_message = announcemented[2]
        client.loop.create_task(sched_message(my_id, my_message, seconds, announcemented[3]))
    else:
        cur.execute("ROLLBACK")
        cur.execute("DELETE FROM announcements WHERE id = %s", (my_id,))

conn.commit()

@client.command()
@commands.has_role("Leadership")
async def quote(ctx, arg):
    for channel in ctx.guild.channels:
        try:
            msg = await channel.fetch_message(int(arg))
            break
        except:
            pass

    embed = discord.Embed(
        title="Quote"
    )
    embed.set_thumbnail(url=msg.author.avatar_url)
    date_string = f"{msg.created_at.day} {msg.created_at.strftime('%B')} {msg.created_at.year}"
    embed.add_field(name=f'"{msg.content}"', value=f"-- {msg.author.mention}, [{date_string}]({msg.jump_url})")
    await ctx.message.delete()
    await ctx.send(embed=embed)
    


client.run(TOKEN)
