import os 
import logging
import telegrampy
from telegrampy.ext import commands
from dotenv import load_dotenv
from findLineup import main_function


logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(levelname)s %(message)s", datefmt="%m/%d/%y - %H:%M:%S %Z")
logger = logging.getLogger("telegrampy")
load_dotenv()

api_token = os.getenv("API_TOKEN")
test_token = os.getenv("TEST_TOKEN")


bot = commands.Bot(api_token)

usage_counter = 0


def show_usage_counter():
    return usage_counter
def show_match(team):
    global usage_counter 
    usage_counter += 1
    if os.path.getsize(f"teams_data/{team}.txt") == 0 :
        return "بازی نداره"   
    
    with open(f"teams_data/{team}.txt", "r", encoding="utf-8") as f:
        file_contents = f.read()
        return file_contents
    
def show_today_match():
    global usage_counter 
    usage_counter += 1
    if os.path.getsize("teams_data/output.txt") > 0 :
        with open("teams_data/output.txt", "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents
    return "امروز بازی نداره"   
    
def show_lineup(team):
    global usage_counter
    usage_counter += 1
    main_function(team)
    if os.path.getsize(f"teams_data/forlineup/{team}lineup.txt") > 0 :
        with open(f"teams_data/forlineup/{team}lineup.txt", "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents
    return "لاین آپ نداریم"   

def show_lastgame(team):
    global usage_counter
    usage_counter += 1
    if os.path.getsize(f"teams_data/latestgames/{team}.txt") > 0:
        with open(f"teams_data/latestgames/{team}.txt", "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents
    else:
        return "نتیجه نداریم"



@bot.command()
async def today(ctx):
    await ctx.send(show_today_match())


#   LINEUP COMMANDS
@bot.command()
async def lineup(ctx, team_code):
    team_code = team_code.lower()
    await ctx.send(show_lineup(team_code), parse_mode="MarkdownV2")


#   SHOW SOCRE OF TEAM'S LATEST GAME
# @bot.command()
# async def last(ctx, team_code):
#     team_code = team_code.lower()
#     await ctx.send(show_lastgame(team_code))

    

#   NATIONAL TEAMS
@bot.command()
async def spa(ctx):
    await ctx.send(show_match("spa"))
@bot.command()
async def eng(ctx):
    await ctx.send(show_match("eng"))
@bot.command()
async def bel(ctx):
    await ctx.send(show_match("bel"))
@bot.command()
async def ned(ctx):
    await ctx.send(show_match("ned"))
@bot.command()
async def ita(ctx):
    await ctx.send(show_match("ita"))
@bot.command()
async def ger(ctx):
    await ctx.send(show_match("ger"))
@bot.command()
async def fra(ctx):
    await ctx.send(show_match("fra"))
@bot.command()
async def por(ctx):
    await ctx.send(show_match("por"))
@bot.command()
async def arg(ctx):
    await ctx.send(show_match("arg"))
@bot.command()
async def bra(ctx):
    await ctx.send(show_match("bra"))


#   SPAIN
@bot.command()
async def atm(ctx):
    await ctx.send(show_match("atm"))
@bot.command()
async def rma(ctx):
    await ctx.send(show_match("rma"))
@bot.command()
async def bar(ctx):
    await ctx.send(show_match("bar"))


#   ENGLAND

@bot.command()
async def ars(ctx):
    await ctx.send(show_match("ars"))
@bot.command()
async def liv(ctx):
    await ctx.send(show_match("liv"))
@bot.command()
async def manu(ctx):
    await ctx.send(show_match("manu"))
@bot.command()
async def manc(ctx):
    await ctx.send(show_match("manc"))
@bot.command()
async def tot(ctx):
    await ctx.send(show_match("tot"))
@bot.command()
async def che(ctx):
    await ctx.send(show_match("che"))

#   ITALY
@bot.command()
async def mil(ctx):
    await ctx.send(show_match("mil"))
@bot.command()
async def int(ctx):
    await ctx.send(show_match("int"))
@bot.command()
async def nap(ctx):
    await ctx.send(show_match("nap"))
@bot.command()
async def juv(ctx):
    await ctx.send(show_match("juv"))

#   FRANCE
@bot.command()
async def psg(ctx):
    await ctx.send(show_match("psg"))


#   GERMANY
@bot.command()
async def bvb(ctx):
    await ctx.send(show_match("bvb"))
@bot.command()
async def bay(ctx):
    await ctx.send(show_match("bay"))

#   IRAN
@bot.command()
async def est(ctx):
    await ctx.send(show_match("est"))
@bot.command()
async def prs(ctx):
    await ctx.send(show_match("prs"))
@bot.command()
async def usagecounter(ctx):
    await ctx.send(show_usage_counter())
bot.run()