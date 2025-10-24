import os 
import logging
import database
from telegrampy.ext import commands
from dotenv import load_dotenv
from findLineup import main_function


class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self):
        ctx = self.context
        # Send a menu with info on the bot
        with open("teams_data/help.txt", "r", encoding="utf-8")as f:
            output = f.read()
        await ctx.send(output, parse_mode="MarkdownV2")
    async def send_cog_help(self, cog):
        ctx = self.context
        # Send a menu with info on the cog passed to the method
        await ctx.send("cog help", parse_mode="MarkdownV2")
    async def send_command_help(self, command):
        ctx = self.context
        # Send a menu with info on the command passed to the method
        await ctx.send("command help", parse_mode="MarkdownV2")

ADMIN_ID = [379177970, 5516117163]

logging.basicConfig(level=logging.DEBUG, format="(%(asctime)s) %(levelname)s %(message)s", datefmt="%m/%d/%y - %H:%M:%S %Z")
logger = logging.getLogger("telegrampy")

load_dotenv()

api_token = os.getenv("API_TOKEN")
test_token = os.getenv("TEST_TOKEN")

bot = commands.Bot(api_token)
bot.help_command = MyHelpCommand()

def show_usage_counter():
    output = database.show_data()
    return output

def show_match(team):
    if os.path.getsize(f"teams_data/next/{team}.txt") == 0 :
        return "بازی نداره"   
    
    with open(f"teams_data/next/{team}.txt", "r", encoding="utf-8") as f:
        file_contents = f.read()
        return file_contents
    
def show_today_match():     
    if os.path.getsize("teams_data/output.txt") > 0 :
        with open("teams_data/output.txt", "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents
    return "امروز بازی نداره"   
    
def show_lineup(team):    
    main_function(team)
    if os.path.getsize(f"teams_data/forlineup/{team}lineup.txt") > 0 :
        with open(f"teams_data/forlineup/{team}lineup.txt", "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents
    return "لاین آپ نداریم"   

def show_lastgame(team):
    if os.path.getsize(f"teams_data/latestgames/{team}.txt") > 0:
        with open(f"teams_data/latestgames/{team}.txt", "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents
    else:
        return "نتیجه نداریم"


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("دستور اشتباه!")
    else:
        await ctx.send(f"Error: {error}")

@bot.command(name="codes")
async def mamad(ctx):
    with open("teams_data/codes.txt", "r", encoding="utf-8") as f:
                output = f.read()
    await ctx.send(output)

@bot.command()
async def today(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_today_match())

@bot.command()
async def lineup(ctx, team_code):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    team_code = team_code.lower()
    await ctx.send(show_lineup(team_code), parse_mode="MarkdownV2")

@bot.command()
async def last(ctx, team_code):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    team_code = team_code.lower()
    await ctx.send(show_lastgame(team_code))

@bot.command()
async def spa(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")  
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("spa"))
@bot.command()
async def eng(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")    
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("eng"))
@bot.command()
async def bel(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("bel"))
@bot.command()
async def ned(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("ned"))
@bot.command()
async def ita(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("ita"))
@bot.command()
async def ger(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("ger"))
@bot.command()
async def fra(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("fra"))
@bot.command()
async def por(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("por"))
@bot.command()
async def arg(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("arg"))
@bot.command()
async def bra(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("bra"))


@bot.command()
async def atm(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("atm"))
@bot.command()
async def rma(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("rma"))
@bot.command()
async def bar(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("bar"))



@bot.command()
async def ars(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("ars"))
@bot.command()
async def liv(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("liv"))
@bot.command()
async def manu(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("manu"))
@bot.command()
async def manc(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("manc"))
@bot.command()
async def tot(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("tot"))
@bot.command()
async def che(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("che"))

@bot.command()
async def mil(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("mil"))
@bot.command()
async def int(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("int"))
@bot.command()
async def nap(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("nap"))
@bot.command()
async def juv(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("juv"))
@bot.command()
async def psg(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("psg"))
@bot.command()
async def bvb(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("bvb"))
@bot.command()
async def bay(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("bay"))
@bot.command()
async def est(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("est"))
@bot.command()
async def prs(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    database.save_data(ctx.author.username, ctx.author.full_name)
    await ctx.send(show_match("prs"))
@bot.command()
async def usagecounter(ctx):
    print(f"( {ctx.author.full_name}@{ctx.author.username} ) hit command /{ctx.command.name}")
    if ctx.author.id in ADMIN_ID:
        await ctx.send(show_usage_counter())
    else:
        database.save_data(ctx.author.username, ctx.author.full_name)
        await ctx.send("2")
bot.run()