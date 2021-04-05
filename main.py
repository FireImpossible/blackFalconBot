# bot.py
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=['bf!', 'Bf!', 'bF!', 'BF!'], intents=intents)
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
        await client.get_channel(text_channel_list[channelname.index("bot-spam")].id).send('Your Best BF is Online') #we've connected to DISCORD!!!!
client.run(TOKEN)
