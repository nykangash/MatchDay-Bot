import datetime
import requests
import schedule
from time import sleep
from persiantools.jdatetime import JalaliDate
import pytz
import emoji
 


#   TODO: better variable names if it's possible
team_id = {
    "rma": "133738",
    "bar": "133739",
    "atm": "133729",
    
    "liv": "133602",
    "manu": "133612",
    "manc": "133613",
    "che" : "133610",
    "ars": "133604",
    "tot": "133616",
    
    "psg": "133714",
    
    "bay": "133664",
    "bvb": "133650",
    
    "int": "133681",
    "mil": "133667",
    "juv": "133676",
    "nap": "133670",
    
    "est": "139012",
    "prs": "139013",
    
    "fra": "133913",
    "ger": "133907",
    "ita": "133910",
    "bel": "134515",
    "eng": "133914",
    "ned": "133905",
    "por": "133908",
    "arg": "134509",
    "bra": "134496",
    "spa": "133909"
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
    """ 
        Converts a UTC timestamp string to a 
        timezone-aware datetime object.
    
    """
    utc_time = datetime.datetime.fromisoformat(gametime_utc_str).replace(tzinfo=pytz.utc)
    target_timezone = pytz.timezone("Asia/Tehran")
    local_time = utc_time.astimezone(target_timezone)
    return local_time


def date_converter(gametime_utc_str):
    """
        Converts a UTC timestamp to Jalali date 
        and weekday in Tehran's timezone.
        
    """
    # Reuse the timezone_convert function to get the local datetime    
    local_datetime = timezone_convert(gametime_utc_str)
    
    # Extract the date and convert to Jalali
    gregorian_date = local_datetime.date()
    jalali_date = JalaliDate.to_jalali(gregorian_date)
    
    # jalali_date.weekday() returns 0 for Saturday
    return jalali_date.weekday(), jalali_date




#   TODO:   clean code with removing this function and the one under this one (_game_updater & _games_sort) 
#           they are probably useless in this state and can be one (MAYBE)


def today_games_updater(game_date):
    '''
        Checks if a game will happen today or not 

        return bool
    '''

    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    if game_date.strftime('%Y-%m-%d') == today_date:
        return True

def today_games_sort(next_game, next_game_datetime):
    games = {}
    
    for i, v in enumerate(next_game):
        try:
            games.setdefault(v , next_game_datetime[i])
        except ValueError:
            continue
    
    games = {k: v for k, v in sorted(games.items(), key=lambda item: item[1])}
    
    
    return games


def next_match_finder():
    '''
        somehow main function...API calls and most of main code is here
    
    '''

    #   CLEAR FILES FOR NEW OUTPUT
    open("teams_data/output.txt", "w").close()
    next_game_list = []
    next_game_datetime_list = []
            
    for team in team_id:
        
        #   CLEAR FILES FOR NEW OUTPUT
        open(f"teams_data/{team}.txt", "w").close()

        
        data = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id={team_id[team]}").json()
        
        if not data or not data["events"]:
            return "دوباره تلاش کنید."
        cleared_data = data["events"][0]
        
        
        game_league = cleared_data["strLeague"]
        

        #   different tournomnet stage namings
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
        separator = "-" * ((len(next_game)*2) + 11)
        is_game_today = today_games_updater(next_game_datetime)



        #   check if game is for today and gather it for /today command
        if is_game_today:
            print(team+ " is Today !!!!")
            next_game_list.append(next_game)
            next_game_datetime_list.append(next_game_datetime.strftime('%H:%M'))


        with open(f"teams_data/{team}.txt", "a", encoding="utf-8") as f:
    #   TODO:   LOOK FOR A BETTER OUTPUT, MAYBE BETTER ALIGNMENT FOR TITLE AND TEAM NAMES
            f.write(
                "# بازی بعدی #\n\n"
                f"{emoji.emojize(":soccer_ball:")} تیم های: {next_game}\n"
                f"{separator}\n"
                f"{emoji.emojize(":trophy:")} مسابقات: {game_league}\n" 
                f"{separator}\n"
                f"{emoji.emojize(":input_numbers:")} دور: {game_round}\n" 
                f"{separator}\n"
                f"{emoji.emojize(":calendar:")} تاریخ: {rooz[weekday]} ({formatted_date})\n"
                f"{separator}\n"
                f"{emoji.emojize(":alarm_clock:")} ساعت: {next_game_datetime.strftime('%H:%M')}\n"
                f"{separator}\n"
                f"{emoji.emojize(":stadium:")} ورزشگاه: {stadium}"
            )
    
        #TODO: better logs
        print(team+" DONE!!!!!")
    
    
    today_sorted_dict = today_games_sort(next_game_list, next_game_datetime_list)
    print("today sorting DONE")
    output_header = True
    separator = "-" * 40#int((len(max(next_game_list, key=len))*2))
    
    for k, v in today_sorted_dict.items():
        if output_header:     
            print("writing output.txt")
            with open("teams_data/output.txt", "a", encoding="utf-8")as f:                 
                f.write(
                        "بازی های امروز\n\n"
                        f"{emoji.emojize(":soccer_ball:")} تیم های: {k}\n"
                        f"{emoji.emojize(":alarm_clock:")} ساعت: {v}\n"  
                        f"{separator}\n"

                        )
            output_header = False
        else:
            print("writing output.txt")
            with open("teams_data/output.txt", "a", encoding="utf-8")as f: 
            
                f.write(
                        f"{emoji.emojize(":soccer_ball:")} تیم های: {k}\n"  
                        f"{emoji.emojize(":alarm_clock:")} ساعت: {v}\n"  
                        f"{separator}\n"
                        
                            )
              
    print("Done at", datetime.datetime.now().strftime("%H:%M"))


# SCHEDULE RUNS
schedule.every().day.at("23:30").do(next_match_finder)
schedule.every().day.at("04:30").do(next_match_finder)
schedule.every().day.at("10:30").do(next_match_finder)
schedule.every().day.at("13:30").do(next_match_finder)
schedule.every().day.at("16:30").do(next_match_finder)
schedule.every().day.at("19:30").do(next_match_finder)

next_match_finder()

while True:
    schedule.run_pending()
    sleep(1)          