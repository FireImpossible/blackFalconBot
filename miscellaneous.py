from bot import *
import random
from fish import *
import csv
from database import *


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
async def merch(ctx):
    person_id = str(ctx.author.id)
    s = []
    try:
        cur.execute("SELECT * FROM GoFishing WHERE user_id = %s", (str(person_id),))
        s = cur.fetchall()
    except:
        await ctx.reply('no data found')
        pass
    
    if len(s) > 0:
        the_person = s[0]
        wormie_num = the_person[2]
        fishie_array = the_person[3]
        fishie_counts = the_person[4]

        fish_display = ''

        for ind in range(0, len(fishie_array)):
            fish_display += f'{fishie_array[ind]} - {fishie_counts[ind]} \n'

        stats_embed = discord.Embed(
                title=f"your fishing stats"
            )
        stats_embed.add_field(name="worm count", value=wormie_num, inline=False)
        stats_embed.add_field(name="fish counts", value=fish_display, inline=False)
        stats_embed.set_thumbnail(url="https://i1.sndcdn.com/artworks-000217345120-79yql0-t500x500.jpg")

        await ctx.reply(embed=stats_embed)

@client.command()
async def gofish(ctx):

    #### CHECK IF USER HAS A WORM
    person_id = str(ctx.author.id)
    s = []
    try:
        cur.execute("SELECT * FROM GoFishing WHERE user_id = %s", (str(person_id),))
        s = cur.fetchall()
    except:
        await ctx.reply('you have no worms...')
        pass
    
    cur.execute("ROLLBACK")
    if len(s) > 0:
        the_person = s[0]
        #print(the_person)
        wormie_num = the_person[2]
        if wormie_num == 0:
            await ctx.reply('you have no worms...')
        else:
            wormie_num -= 1
            your_worms = wormie_num
            ##update worm number in user row
            cur.execute("UPDATE GoFishing SET worm_count = %s WHERE user_id = %s", (wormie_num, person_id))
           
            fishie_array = the_person[3]
            fishie_counts = the_person[4]

            rand_num = random.randint(0, (len(fish_names) - 1))
            rand_fish = fish_names[rand_num]
            rand_pic = fish_img[rand_num]
            
            if rand_fish in fishie_array:
                ind = fishie_array.index(rand_fish)
                now_fish = fishie_counts[ind] + 1
                fishie_counts[ind] = now_fish
            else:
                fishie_array.append(rand_fish)
                fishie_counts.append(1)
            
            cur.execute("UPDATE GoFishing SET owned_fish = %s WHERE user_id = %s", (fishie_array, person_id))
            cur.execute("UPDATE GoFishing SET fish_counts = %s WHERE user_id = %s", (fishie_counts, person_id))
            
            conn.commit()

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

                ##select user id
                your_worms = 1
                person_id = str(ctx.author.id)
                s = []
                
                try:
                    cur.execute("SELECT * FROM GoFishing WHERE user_id = %s", (str(person_id),))
                    s = cur.fetchall()
                except:
                    pass
                cur.execute("ROLLBACK")
                if len(s) > 0:
                    ##get the value for the worm from the row
                    the_person = s[0]
                    wormie_num = the_person[2]
                    ##add one to worm number
                    wormie_num += 1
                    your_worms = wormie_num
                    ##update worm number in user row
                    cur.execute("UPDATE GoFishing SET worm_count = %s WHERE user_id = %s", (wormie_num, person_id))

                else:

                    ##if user id isn't in the database, add them and create a blank entry
                    cur.execute("INSERT INTO GoFishing (user_id, worm_count, owned_fish, fish_counts) VALUES(%s, %s, %s, %s)", (person_id, 1, [], []))
                
                await ctx.reply(f'you get one knowledge wormie! :worm: now you have {your_worms} worms')
                #await ctx.reply(f'you get one knowledge wormie! now you have {worm_count} worms :worm:')
                conn.commit()
                client.in_session = False
                
            elif my_answer == "quit":
                await ctx.reply('better luck next time \🐟')
                client.in_session = False
            else:
                await ctx.reply('quit or try again \✨')


# cur.execute("CREATE TABLE GoFishing (id SERIAL PRIMARY KEY , user_id text, worm_count integer, owned_fish text[], fish_counts integer[]);")
# conn.commit()
