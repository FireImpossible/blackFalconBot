from bot import *

import random
import datetime
import asyncio

from badWords import *
from manage_timezones import convertDateTime

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    user= await client.get_user_info("324362342026444800")
    await client.send_message(user, "hola senior")
    # thien's thing:
    for guild in client.guilds:
        print(guild.name)
        text_channel_list = []
        channelname = []
        for channel in guild.channels:  # getting all channels in the servers
            print(str(channel.name) + " type: " + str(channel.type))
            if str(channel.type).lower() == 'text':  # if it's a text channel
                text_channel_list.append(channel)  # gets actual channel
                channelname.append(channel.name)  # gets channel name
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
                await client.get_channel(LOG_CHANNEL_ID).send(
                    f"{message.author} decided to be naughty and said a bad word!")
                await message.delete()
                return
    await client.process_commands(message)


async def gm_message():
    message_hour = 7
    message_minute = 25

    wakey_messages = ['early birdies get the wormies', 'wake up eggies, stretch your leggies',
                      "get up hatchlings or you'll need patchlings", 'come on falcons, make some palcons',
                      'leave the nest, or youll have nothing left', 'wakey wakey eggs and bakey',
                      'get out of beddies if youre not deddies', 'time for yall eggies to get cracking',
                      'wake up late and youre falcon bait', 'rise and shine or they will dine',
                      'if youre not awake youll be baked', 'sleep is canceled so you dont get scrambled']

    right_now = datetime.datetime.now()  # - datetime.timedelta(hours=time_zone) remove this to implement autotimezone
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
        time_dif = (convertDateTime(
            datetime.datetime(2021, month, day, message_hour, message_minute, 0)) - datetime.datetime(2021, month, day,
                                                                                                      hour, minute,
                                                                                                      second)).total_seconds()
        ##schedule for those secs
    else:
        ##how long has passed since 8 am
        time_dif = (datetime.datetime(2021, month, day, hour, minute, second) - datetime.datetime(2021, month, day,
                                                                                                  message_hour,
                                                                                                  message_minute,
                                                                                                  0)).total_seconds()
        time_dif = 86400 - time_dif

    await asyncio.sleep(time_dif)

    ##randomize a method
    message = wakey_messages[random.randint(0, (len(wakey_messages) - 1))]

    for guild in client.guilds:
        text_channel_list = []
        channelname = []
        for channel in guild.channels:  # getting all channels in the servers
            if str(channel.type).lower() == 'text':  # if it's a text channel
                text_channel_list.append(channel)  # gets actual channel
                channelname.append(channel.name)  # gets channel name
        await client.get_channel(text_channel_list[channelname.index("cargo-hold")].id).send(
            message)  # we've connected to DISCORD!!!!

    while True:
        await asyncio.sleep(86400)

        ##randomize a method
        message = wakey_messages[random.randint(0, (len(wakey_messages) - 1))]

        for guild in client.guilds:
            text_channel_list = []
            channelname = []
            for channel in guild.channels:  # getting all channels in the servers
                if str(channel.type).lower() == 'text':  # if it's a text channel
                    text_channel_list.append(channel)  # gets actual channel
                    channelname.append(channel.name)  # gets channel name
            await client.get_channel(text_channel_list[channelname.index("bot-spam")].id).send(
                message)  # we've connected to DISCORD!!!!
