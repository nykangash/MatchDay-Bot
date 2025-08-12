import logging
import requests
import telegrampy
from telegrampy.ext import commands
import datetime
import pytz
from persiantools.jdatetime import JalaliDate

logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(levelname)s %(message)s", datefmt="%m/%d/%y - %H:%M:%S %Z")
logger = logging.getLogger("telegrampy")

# Replace this with your actual bot token
bot = commands.Bot("API_TOKEN")

team_id = {
    "liv": "133602",
    "rma": "133738",
    "mnu": "133612",
    "psg": "133714",
    "bay": "133664"
}
# Persian weekday names mapped to JalaliDate.weekday() output (0=شنبه)
rooz = {
    0: "شنبه",
    1: "یکشنبه",
    2: "دوشنبه",
    3: "سه‌شنبه",
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
    
    next_game = cleared_data["strEvent"]
    next_game_datetime = timezone_convert(cleared_data["strTimestamp"])
    
    weekday, next_game_date = date_converter(cleared_data["strTimestamp"])
    formatted_date = next_game_date.strftime("%B %d") 

    return (
        f"{next_game}\n"
        f"{rooz[weekday]}\n"
        f"تاریخ: {formatted_date}\n"
        f"ساعت: {next_game_datetime.strftime('%H:%M')}"
    )

@bot.command()
async def rma(ctx):
    await ctx.send(next_match_finder("rma"))

@bot.command()
async def liv(ctx):
    await ctx.send(next_match_finder("liv"))

@bot.command()
async def psg(ctx):
    await ctx.send(next_match_finder("psg"))

@bot.command()
async def mnu(ctx):
    await ctx.send(next_match_finder("mnu"))

@bot.command()
async def bay(ctx):
    await ctx.send(next_match_finder("bay"))


bot.run()