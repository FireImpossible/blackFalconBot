from bot import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
from soup_functions import *


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
    competition_embed.set_thumbnail(
        url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png")
    competition_embed.set_footer(text=f"Viewing page {page_num} of 2.")

    # flavor the soup
    if page_num == 1:  # page 1
        trainEvents = tablebody[0].find_all("tr")
        eventObj = getEvents(trainEvents)
        for x in range(1, int(len(eventObj) / 2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False)
    else:  # page 2
        roundEvents = tablebody[1].find_all("tr")
        eventObj = getEvents(roundEvents)
        for x in range(int(len(eventObj) / 2)):
            competition_embed.add_field(name=eventObj[x * 2], value=eventObj[(x * 2) + 1], inline=False)

    # send the soup
    await ctx.send(embed=competition_embed)


@client.command(aliases=['pt', 'packet_tracer', 'mods', 'h*ll'])
async def cisco(ctx, *args):
    # stolen
    url = "https://www.uscyberpatriot.org/competition/current-competition/challenges-by-round"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tablebody = soup.find_all("tbody")[1].find_all("tr")

    ##set up some dictionary
    mod_dict = {}
    test_string = ''
    for trCount in range(0, len(tablebody)):

        strong = tablebody[trCount].find(lambda tag: tag.name == 'td' and "Round" in tag.text)

        ##for every <strong> tag that's found
        if strong:
            key = strong.get_text()
            mod_dict[key] = ''
            test_string += '\n' + str(key)  # testing

            ## search trs until next td with strong + round is found
            trMod = trCount + 1
            next_strong = tablebody[trMod].find(lambda tag: tag.name == 'td' and "Round" in tag.text)

            while not next_strong and trMod < len(tablebody) - 1:
                # for trMod in range(trCount + 1, len(tablebody)):

                module = tablebody[trMod].find(lambda tag: tag.name == 'td' and "Module" in tag.text)
                ##search until the text in the tr tag has the text "module"
                if module:
                    mod_dict[key] += '\n' + str(module.get_text())
                    test_string += '\n' + str(module.get_text())
                    ##add to dictionary
                trMod += 1
                next_strong = tablebody[trMod].find(
                    lambda tag: tag.name == 'td' and "Round" in tag.text)  # recursion potential

    ##for each key in dict... make an embed
    cisco_embed = discord.Embed(
        title=f"cisco mods <3:"
    )
    cisco_embed.set_thumbnail(
        url="https://www.saashub.com/images/app/service_logos/51/4ef1468caaa3/large.png?1558762812")
    for key in mod_dict.keys():
        cisco_embed.add_field(name=key, value=mod_dict[key], inline=False)

    await ctx.send(embed=cisco_embed)

@client.command(aliases=['scores'])
async def score(ctx, *args):
    value = str(args[0])
    if value == "white":
        value = "14-0792"
    elif value == "red":
        value = "14-0791"
    elif value == "purple":
        value = "14-0790"
    elif value == "black":
        value = "14-0789"
    teamId = value #"14-0792"
    teamResult = getScore(teamId)
    #scores = "Total Score for Team " + teamResult["id"] + ": " + str(teamResult["total"])
    score_embed = discord.Embed(
         title=f"Score"
    )
    score_embed.set_thumbnail(
        url="https://www.kindpng.com/picc/m/136-1363669_afa-cyberpatriot-hd-png-download.png")
    for key in teamResult.keys():
        if teamResult[key] != "":
            score_embed.add_field(name=key, value=teamResult[key], inline=False)
    await ctx.send(embed=score_embed)
