from bot import *
import random
from fish import *
import csv

magic_ball_responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes – definitely.", "You may rely on it."]


fishing = {
    'mollyyan': {
        'fish': ['Crappie', 'Weakfish'],
        'worms': 500
    }
}

@client.command(name="8ball")
async def _8ball(ctx):
    await ctx.reply(random.choice(magic_ball_responses))

@client.command()
async def ping(ctx):
    await ctx.reply("pong!")
    if ctx.message.author.has_role("Leadership"):
        await ctx.reply("AHHHHHH")

@client.command()
async def yeehaw(ctx):
    await ctx.reply("cowbois \🤠")

@client.command()
async def gofish(ctx):

    #### CHECK IF USER HAS A WORM
    ##get id of user that sent message
    ##select the row from the database
    ##get worm count
    ##if worm count > 0, run this

    rand_num = random.randint(0, (len(fish_names) - 1))
    rand_fish = fish_names[rand_num]
    rand_pic = fish_img[rand_num]
    fish_embed = discord.Embed(
        title=f"You caught a {rand_fish} \✨"
    )
    if rand_fish == "Crappie" or rand_fish == "Weakfish":
      fish_embed.add_field(name="please be kind", value="all fish can become a catch with your love and support \🥰", inline=False)
    fish_link = "[all about the " + rand_fish + "](https://fishingbooker.com/fish/" + rand_pic + ")"
    fish_embed.add_field(name="learn more!", value=fish_link, inline=False)
    fish_embed.set_image(
        url=f"https://static.fishingbooker.com/public/images/fish/275x160/{rand_pic}.png")
    await ctx.reply(embed=fish_embed)

    #### DELETE ONE WORM FROM THE USER'S DATA BASE
    ##worm count - 1
    ##update user data base

    #### SAVE FISH TO USER'S DATABASE
    ##get array of fish
    ##get array of fish counts
    ##check if fish exist in array
    ##if exist
        ##add 1 to the corresponding fish counts index
    ##if not exist
        ##append fish name
        ##append 1 to fish count

client.in_session = False
@client.command()
async def wormie(ctx, *args):

    ubuntu = ["Ubuntu", "ubuntu", "u"]
    windows = ["Windows", "windows", "w"]
    pt = ["PT", "pt", "cisco", "packet", "Packet", "Cisco"]
    if not client.in_session:
        client.in_session = True

        ##did the user specify an operating system?
        user_os = ""
        if args:
            if args[0] in ubuntu:
                user_os = "Ubuntu"
            elif args[0] in pt:
                user_os = "PT"
            elif args[0] in windows:
                user_os = "Windows"
            else:
                pass
        
        ##start question asking
        question = ""
        answer = ""
        worm_os = ""

        ###generate worm question
        all_wormies = []
        with open('knowledge_wormies.csv', newline='') as csvfile:
            all_wormies = list(csv.reader(csvfile))
        
        rand_worm = random.randint(1, (len(all_wormies) - 1))
        row = all_wormies[rand_worm]
        worm_os = row[2]

        if not user_os == "":
            while user_os != worm_os:
                rand_worm = random.randint(1, (len(all_wormies) - 1))
                row = all_wormies[rand_worm]
                worm_os = row[2]
                
            
        question = row[0]
        answer = row[1]

        ##ask the user the worm question
        question_embed = discord.Embed(
            title=f"Answer correctly and get a worm!"
        )   
        question_embed.set_thumbnail(
            url="https://icon-library.com/images/worm-icon/worm-icon-9.jpg")
        question_embed.add_field(name=worm_os, value=question, inline=False)
        await ctx.reply(embed=question_embed)

        my_answer = ""
        while my_answer != answer and my_answer != "quit":
            #my_response = await client.wait_for("message")
            msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            
            my_answer = msg.content.lower()
            #my_user = my_response.use
            if my_answer == answer:
                # user_data = fishing['mollyyan']
                # worm_count = user_data['worms'] 
                # user_data['worms'] = worm_count + 1
                # worm_count = user_data['worms']

                # print(ctx.author.id)
                ##if user id isn't in the database, add them and create a blank entry
                ##select user id
                ##get the value for the worm from the row
                ##add one to worm number
                ##update worm number in user row
                
                await ctx.reply('you get one knowledge wormie! :worm:')
                #await ctx.reply(f'you get one knowledge wormie! now you have {worm_count} worms :worm:')
                client.in_session = False
                
            elif my_answer == "quit":
                await ctx.reply('better luck next time \🐟')
                client.in_session = False
            else:
                await ctx.reply('quit or try again \✨')

@client.command()
async def stats(ctx):
    ##get user id
    ##select row from table with user id
    ##create embeds

    ##if args fishies
        ##get fish array
        ##get fish counts
        ##for each in range len(fish_array)
            ##add field for fish name + fish counts
    ##no args
        ##get total fish
        ##get total wormies
        ##add fields
    pass

# cur.execute("CREATE TABLE Fishing (id SERIAL PRIMARY KEY , user_id integer, worm_count integer, owned_fish text[], fish_counts integer[]);")
