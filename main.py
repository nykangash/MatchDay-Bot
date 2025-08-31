import os 
import logging
import requests
import telegrampy
from telegrampy.ext import commands
import datetime
import pytz
from persiantools.jdatetime import JalaliDate
from dotenv import load_dotenv
import emoji


logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(levelname)s %(message)s", datefmt="%m/%d/%y - %H:%M:%S %Z")
logger = logging.getLogger("telegrampy")
load_dotenv()

api_token = os.getenv("API_TOKEN")
test_token = os.getenv("TEST_TOKEN")
seperator = "-------------------------------------------------------------"

# Replace this with your actual bot token
bot = commands.Bot(api_token)

team_id = {
    "liv": "133602",
    "rma": "133738",
    "mnu": "133612",
    "psg": "133714",
    "bay": "133664",
    "est": "139012",
    "prs": "139013",
    "fcb": "133739",
    "mnc": "133613",
    "ars": "133604",
    "tot": "133616",
    "acm": "133667",
    "int": "133681",
    "bvb": "133650",
    "atm": "133729",
    "juv": "133676",
    "nap": "133670"
}
# Persian weekday names mapped to JalaliDate.weekday() output (0=شنبه)
rooz = {
    0: "شنبه",
    1: "یکشنبه",
    2: "دوشنبه",
    3: "سه‌ شنبه",
    4: "چهارشنبه",
    5: "پنجشنبه",
    6: "جمعه"
}

def timezone_convert(gametime_utc_str):
    """Converts a UTC timestamp string to a timezone-aware datetime object."""
    utc_time = datetime.datetime.fromisoformat(gametime_utc_str).replace(tzinfo=pytz.utc)
    target_timezone = pytz.timezone("Asia/Tehran")
    local_time = utc_time.astimezone(target_timezone)
    return local_time

def date_converter(gametime_utc_str):
    """Converts a UTC timestamp to Jalali date and weekday in Tehran's timezone."""
    # Reuse the timezone_convert function to get the local datetime
    local_datetime = timezone_convert(gametime_utc_str)
    
    # Extract the date and convert to Jalali
    gregorian_date = local_datetime.date()
    jalali_date = JalaliDate.to_jalali(gregorian_date)
    
    # jalali_date.weekday() returns 0 for Saturday
    return jalali_date.weekday(), jalali_date

def next_match_finder(team):
    data = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id={team_id[team]}").json()
    
    if not data or not data["events"]:
        return "No upcoming matches found."
        
    cleared_data = data["events"][0]
    
    
    game_league = cleared_data["strLeague"]
    
    if cleared_data["intRound"] == "200":
        game_round =  "فینال"
    elif cleared_data["intRound"] == "150":
        game_round = "نیمه نهایی"
    elif cleared_data["intRound"] == "125":
        game_round = "یک چهارم نهایی" 
    elif "League" in cleared_data["strLeague"] or "Ligue" in cleared_data["strLeague"] or "Liga" in cleared_data["strLeague"]:
        game_round = f"هفته {cleared_data["intRound"]} "
    else:
        game_round = cleared_data["intRound"]
    
    
    next_game = cleared_data["strEvent"]
    next_game_datetime = timezone_convert(cleared_data["strTimestamp"])
    
    weekday, next_game_date = date_converter(cleared_data["strTimestamp"])
    formatted_date = next_game_date.strftime("%B %d") 
    stadium = cleared_data["strVenue"]
    return (
        f"# بازی بعدی #\n\n"
        f"{emoji.emojize(":soccer_ball:")} تیم های: {next_game}\n"
        f"{seperator}\n"
        f"{emoji.emojize(":trophy:")} مسابقات: {game_league}\n" 
        f"{seperator}\n"
        f"{emoji.emojize(":input_numbers:")} دور: {game_round}\n" 
        f"{seperator}\n"
        f"{emoji.emojize(":calendar:")} تاریخ: {rooz[weekday]} ({formatted_date})\n"
        f"{seperator}\n"
        f"{emoji.emojize(":alarm_clock:")} ساعت: {next_game_datetime.strftime('%H:%M')}\n"
        f"{seperator}\n"
        f"{emoji.emojize(":stadium:")} ورزشگاه: {stadium}"
    )


#   SPAIN
@bot.command()
async def atm(ctx):
    await ctx.send(next_match_finder("atm"))
@bot.command()
async def rma(ctx):
    await ctx.send(next_match_finder("rma"))
@bot.command()
async def fcb(ctx):
    await ctx.send(next_match_finder("fcb"))


#   ENGLAND
@bot.command()
async def ars(ctx):
    await ctx.send(next_match_finder("ars"))
@bot.command()
async def liv(ctx):
    await ctx.send(next_match_finder("liv"))
@bot.command()
async def mnu(ctx):
    await ctx.send(next_match_finder("mnu"))
@bot.command()
async def mnc(ctx):
    await ctx.send(next_match_finder("mnc"))
@bot.command()
async def tot(ctx):
    await ctx.send(next_match_finder("tot"))


#   ITALY
@bot.command()
async def acm(ctx):
    await ctx.send(next_match_finder("acm"))
@bot.command()
async def intm(ctx):
    await ctx.send(next_match_finder("int"))
@bot.command()
async def nap(ctx):
    await ctx.send(next_match_finder("nap"))
@bot.command()
async def juv(ctx):
    await ctx.send(next_match_finder("juv"))

#   FRANCE
@bot.command()
async def psg(ctx):
    await ctx.send(next_match_finder("psg"))


#   GERMANY
@bot.command()
async def bvb(ctx):
    await ctx.send(next_match_finder("bvb"))
@bot.command()
async def bay(ctx):
    await ctx.send(next_match_finder("bay"))


#   IRAN
@bot.command()
async def est(ctx):
    await ctx.send(next_match_finder("est"))
@bot.command()
async def prs(ctx):
    await ctx.send(next_match_finder("prs"))
    


bot.run()