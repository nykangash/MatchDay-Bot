import os 
import logging
import telegrampy
from telegrampy.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(levelname)s %(message)s", datefmt="%m/%d/%y - %H:%M:%S %Z")
logger = logging.getLogger("telegrampy")
load_dotenv()

api_token = os.getenv("API_TOKEN")
test_token = os.getenv("TEST_TOKEN")


# Replace this with your actual bot token
bot = commands.Bot(api_token)


# Persian weekday names mapped to JalaliDate.weekday() output (0=شنبه)

def show_match(team):
    if os.path.getsize(f"teams_data/{team}.txt") == 0 :
        return "بازی نداره"   
    
    with open(f"teams_data/{team}.txt", "r", encoding="utf-8") as f:
        file_contents = f.read()
        return file_contents
    
def show_today_match():
    if os.path.getsize("teams_data/output.txt") > 0 :
        with open("teams_data/output.txt", "r", encoding="utf-8") as f:
            file_contents = f.read()
            return file_contents
    return "امروز بازی نداره"   
    
        
    



@bot.command()
async def today(ctx):
    await ctx.send(show_today_match())

#   NATIONAL TEAMS
@bot.command()
async def spn(ctx):
    await ctx.send(show_match("spn"))
@bot.command()
async def eng(ctx):
    await ctx.send(show_match("eng"))
@bot.command()
async def blg(ctx):
    await ctx.send(show_match("blg"))
@bot.command()
async def net(ctx):
    await ctx.send(show_match("net"))
@bot.command()
async def itl(ctx):
    await ctx.send(show_match("itl"))
@bot.command()
async def grm(ctx):
    await ctx.send(show_match("grm"))
@bot.command()
async def frc(ctx):
    await ctx.send(show_match("frc"))
@bot.command()
async def por(ctx):
    await ctx.send(show_match("por"))
@bot.command()
async def arg(ctx):
    await ctx.send(show_match("arg"))
@bot.command()
async def brz(ctx):
    await ctx.send(show_match("brz"))






#   SPAIN
@bot.command()
async def atm(ctx):
    await ctx.send(show_match("atm"))
@bot.command()
async def rma(ctx):
    await ctx.send(show_match("rma"))
@bot.command()
async def fcb(ctx):
    await ctx.send(show_match("fcb"))


#   ENGLAND

@bot.command()
async def ars(ctx):
    await ctx.send(show_match("ars"))
@bot.command()
async def liv(ctx):
    await ctx.send(show_match("liv"))
@bot.command()
async def mnu(ctx):
    await ctx.send(show_match("mnu"))
@bot.command()
async def mnc(ctx):
    await ctx.send(show_match("mnc"))
@bot.command()
async def tot(ctx):
    await ctx.send(show_match("tot"))


#   ITALY
@bot.command()
async def acm(ctx):
    await ctx.send(show_match("acm"))
@bot.command()
async def intm(ctx):
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
    


bot.run()