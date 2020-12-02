import discord
from discord.ext import commands
from covid import Covid
import os
cov = Covid(source="john_hopkins")
bot = commands.Bot(command_prefix='$',case_insensitive=True)
Token=int(os.environ.get('TOKEN',3))

@bot.event
async def on_ready():
    game = discord.Game("The Waiting Game")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print('Hello')

@bot.event
async def on_join():
    print('The source of all your Covid-19 data quueries has arrived')

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("Command Doesn't Exist")

@bot.command()
async def clear(ctx,amount:int):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def Data(ctx,coun):
    embed=discord.Embed(
        title = 'Covid Data about '+ coun,
        description='',
        color= discord.Color.dark_gold()
    )
    data=cov.get_status_by_country_name(coun)
    def Val(k):
        for key, value in data.items():
            if k == key:
                return value
    embed.set_footer(text=cov.source)
    embed.set_thumbnail(url='https://ahmednafies.github.io/covid/img/corona.jpeg')
    embed.set_image(url='https://ahmednafies.github.io/covid/img/corona.jpeg')
    embed.set_author(name='Covid Data',
                    icon_url='https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg')
    embed.add_field(name='Total Confirmed Cases', value=Val('confirmed'), inline=False)
    embed.add_field(name='Active Cases',value=Val('active'),inline=False)
    embed.add_field(name='No.of Deaths', value=Val('deaths'), inline=False)
    embed.add_field(name='Recovered', value=Val('recovered'), inline=False)
    await ctx.send(embed=embed)

@Data.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('That country is not in our list please try again')

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please pass all needed arguments ")

@bot.command()
async def helpme(ctx):
    embed = discord.Embed(
        title='HELP HAS ARRIVED!!',
        color=discord.Color.purple()
    )
    embed.set_footer(text=cov.source)
    embed.set_thumbnail(url='https://ahmednafies.github.io/covid/img/corona.jpeg')
    embed.set_author(name='Covid Data',
                    icon_url='https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg')
    embed.add_field(name='Cant find data on a country?', value="If it has a space in its name be sure to put it in quotes", inline=False)
    embed.add_field(name='The quotes have failed you?',value="You've probably entered a country where data isn't public , because the API in use has over 400 countries and counting!", inline=False)
    await ctx.send(embed=embed)

bot.run(Token)
