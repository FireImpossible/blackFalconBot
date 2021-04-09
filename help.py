from bot import *

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
