from bot import *
import random
from fish import *

magic_ball_responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes – definitely.", "You may rely on it."]


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
    rand_num = random.randint(0, (len(fish_names) - 1))
    rand_fish = fish_names[rand_num]
    rand_pic = fish_img[rand_num]
    fish_embed = discord.Embed(
        title=f"You caught a {rand_fish}"
    )
    # file = discord.File("path/to/image/file.png", filename="image.png")
    # fish_embed.set_image(url=f"fish_pics://{rand_pic}.png")
    fish_embed.set_thumbnail(
        url=f"https://static.fishingbooker.com/public/images/fish/275x160/{rand_pic}.png")
    await ctx.reply(embed=fish_embed)
