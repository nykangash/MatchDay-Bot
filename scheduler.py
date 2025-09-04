import datetime
import requests
import schedule
from time import sleep
from persiantools.jdatetime import JalaliDate
import pytz
import emoji
 



seperator = "-------------------------------------------------------"
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
    "nap": "133670",
    "frc": "133913",
    "grm": "133907",
    "itl": "133910",
    "blg": "134515",
    "eng": "133914",
    "net": "133905",
    "por": "133908",
    "arg": "134509",
    "brz": "134496",
    "spn": "133909"
}

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

def today_games_updater(game_date):
    #   updates output.txt everyday at 00:00 for football games of that day (if no game:  return "str" will happen in main script)

    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    if game_date.strftime('%Y-%m-%d') == today_date:
        return True



def next_match_finder():
    open("teams_data/output.txt", "w").close()

    for team in team_id:
        
        #   clears team file
        open(f"teams_data/{team}.txt", "w").close()

        
        data = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id={team_id[team]}").json()
        
        if not data or not data["events"]:
            return "دوباره تلاش کنید."
            
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
        
        is_game_today = today_games_updater(next_game_datetime)
        if is_game_today:
            print(team + " is today !")
            with open("teams_data/output.txt", 'a')as f: 
                f.write(cleared_data["strEvent"]+ "\n" + next_game_datetime.strftime('%H:%M') +  "\n" + seperator + "\n")

        with open(f"teams_data/{team}.txt", "a", encoding="utf-8") as f:

            f.write(
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
            print(team+" DONE!!!!!")
        
    
schedule.every().day.at("04:00").do(next_match_finder)

while True:
    schedule.run_pending()
    sleep(1)