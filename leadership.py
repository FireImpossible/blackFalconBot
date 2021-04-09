from bot import *
from database import *
from manage_timezones import *
import asyncio


@client.command()
@commands.has_role("botDev")
async def announce(ctx, *args):
    text = ""
    if not args:
        return
    else:  # put the whole thing into a string
        for arg in args:
            text += arg + " "

    desired_guild = ctx.guild
    text_channel_list = []
    channelname = []
    for channel in desired_guild.channels:  # getting all channels in the servers
        if str(channel.type).lower() == 'text':  # if it's a text channel
            text_channel_list.append(channel)  # gets actual channel
            channelname.append(channel.name)  # gets channel name
    await client.get_channel(text_channel_list[channelname.index("random-announcement-channel")].id).send(text) # we've connected to DISCORD!!!!


def delete_scheduled(my_id):
    message = "Announcement " + str(my_id) + " has been deleted"
    try:
        cur.execute("DELETE FROM announcements WHERE id = %s", (my_id,))
    except:
        message = "That message doesn't exist!"
    return message


@client.command()
@commands.has_role("botDev")
async def schedule(ctx, *args):
    text = ""
    time_string = ""
    date = []
    time = []
    if not args:
        return
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
            if len(time) == 3:  # includes seconds
                my_time = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1]),
                                            int(time[2]))
            else:  # doesn't include seconds
                my_time = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1]))
            # set the text
            for arg in args[2:]:
                text += arg + " "
            time_string = f"{time[0]}:{time[1]} am"
        except:
            exception_embed = discord.Embed(
                title=f"You're fukcing wrong \✨"
            )
            exception_embed.add_field(name="**The** ***CORRECT***  **Syntax**",
                                      value="bf!schedule <MM/DD/YYYY> <HH:MM> <announcement>")
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
        await ctx.send("Your time has already passed, change it to some time in the future")
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
    await message_send(ctx.guild, message_id, "getting-rank", text)

def get_scheduled(guild, page):
    cur.execute("SELECT * FROM announcements WHERE guildName = %s", (str(guild),))
    announce = cur.fetchall()

    sched_embed = discord.Embed(
        title=f"Scheduled Announcements:"
    )

    max_pages = round(len(announce) / 10)

    if (page > max_pages): page = max_pages
    # competition_embed.set_thumbnail(url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png")
    sched_embed.set_footer(text=f"Viewing page {page + 1} out of {max_pages + 1}.")

    page_start = (page) * 10
    page_end = page_start + 9

    if (page == max_pages):
        page_end = len(announce)

    for x in range(page_start, page_end):
        announcemented = announce[x]
        my_id = announcemented[0]
        my_date = str(announcemented[1])
        my_message = announcemented[2]

        schedule_shower = my_message + " scheduled for " + my_date
        sched_embed.add_field(name=my_id, value=schedule_shower, inline=False)

    # for announcemented in announce:

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

# @client.event ###how do you do it so its when the bot joins, is it broken in general, why is the ctx underlined

async def message_send(guild, row, channel_name, message):
    text_channel_list = []
    channelname = []

    for g in client.guilds:
        if g.name == guild:
            guild = g
    for channel in guild.channels:  # getting all channels in the servers
        if str(channel.type).lower() == 'text':  # if it's a text channel
            text_channel_list.append(channel)  # gets actual channel
            channelname.append(channel.name)  # gets channel name
    # check if still send message
    cur.execute("SELECT * FROM announcements")
    s = cur.fetchall()
    for x in s:
        if row in x:
            await client.get_channel(text_channel_list[channelname.index(channel_name)].id).send(message)  # we've connected to DISCORD!!!!
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
@commands.has_role("botDev")
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

