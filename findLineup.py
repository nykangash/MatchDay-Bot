import json
import re
import requests
import logging
from data import team_names_flashscore, team_fullname, teamid_flashscore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

match_id = ""
def prepare_for_search(teamname):
    return teamname.replace(" ", "-").lower()

def main_function(team_kochoolo):
        global match_id
        next_game_data = requests.get(f"https://www.flashscore.com/team/{team_names_flashscore[team_kochoolo]}/{teamid_flashscore[team_kochoolo]}/").text


        # Escape the team name to handle special regex characters (like . or +)
        pattern = r"(?<=,\s)[A-Z][A-Za-zÀ-ÿ0-9\s.'-]+?\s(?:v|vs\.?|vs)\s[A-Z][A-Za-zÀ-ÿ0-9\s.'-]+?(?=\s+live\b)"

        match = re.search(pattern, next_game_data)
        if match:
            opponent_team = match.group()
            # print(opponent_team)
        opponent_team_cleaned = [item.strip() for item in opponent_team.split(" v ") if item.strip().lower().replace(" ","-") not in team_names_flashscore[team_kochoolo]]
        logger.info(f"Opponent name found => {opponent_team_cleaned[0]}")

        if opponent_team_cleaned[0] in team_fullname.values():
            logger.info("Opponent is found in database")
            opponent_short_name =  list(team_fullname.keys())[list(team_fullname.values()).index(opponent_team_cleaned[0])]
            game_data = requests.get(f"https://www.flashscore.com/match/football/{team_names_flashscore[opponent_short_name]}-{teamid_flashscore[opponent_short_name]}/{team_names_flashscore[team_kochoolo]}-{teamid_flashscore[team_kochoolo]}/").text
            
        else:
            team_kiri = prepare_for_search(opponent_team_cleaned[0])    
            search_data = requests.get(f"https://s.livesport.services/api/v2/search/?q={team_kiri}&lang-id=1&type-ids=1,2,3,4&project-id=2&project-type-id=1").text
            jsoned = json.loads(search_data)
            team_kiri_id = jsoned[0]["id"]
            team_kiri_flashscore_name = jsoned[0]["url"]
            
            game_data = requests.get(f"https://www.flashscore.com/match/football/{team_kiri_flashscore_name}-{team_kiri_id}/{team_names_flashscore[team_kochoolo]}-{teamid_flashscore[team_kochoolo]}/").text
            

        pattern = r'"event_id_c":"(.*?)"'

        match = re.search(pattern, game_data)
        if match:
            match_id = match.group().split(":")[1]
            match_id = match_id.replace('"', '')
            logger.info(f"Match-ID Found => {match_id}")
        else:
            logger.info("Can't find any eventID...\n\n")
        predicted_lineup = "dplie"
        lineup = "dlie2"

        try:
            players_data = requests.get(f"http://2.ds.lsapp.eu/pq_graphql?_hash={lineup}&eventId={match_id}&projectId=2").json()
            findbyid = players_data["data"]
            eventpartic = findbyid["findEventById"]
            typename = eventpartic["eventParticipants"]
            open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "w").close
            if len(typename[1]["lineup"]["players"])> 0:
                lineup1 = typename[1]["lineup"]
                lineup2 = typename[0]["lineup"]
                players1 = lineup1["players"]
                players2 = lineup2["players"]
                logger.info("Official lineup Found !!! ")
                output_header = True
                team1_width =  len(max(players1, key=lambda x: len(x["fieldName"]))["fieldName"])
                team2_width =  len(max(players2, key=lambda x: len(x["fieldName"]))["fieldName"])
                if output_header:
                    with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "w", encoding="utf-8")as writeit:
                        writeit.write(
                            '```\nترکیب رسمی\n\n\n'
                            f'{typename[1]["name"]:<{team1_width}}' f'{team_fullname[team_kochoolo]:<{team2_width}}\n'.rjust(20, " ")                        
                                        )
                    output_header = False
                with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "a", encoding="utf-8")as writeit:
                    # name_width_team1 = max(len())
                    lineup_counter = 1
                    for i1, i2 in zip(players1, players2):
                        if lineup_counter <= 11:
                            lineup_counter +=1
                            writeit.write(
                                f'{i1["number"]:>2} {i1["fieldName"]:<{team1_width}}'                            f'     {i2["fieldName"]:<{team2_width}} {i2["number"]:>2}\n'.rjust(20," ")
                                
                                            )
                        else:
                            break
                    writeit.write("```")
                logger.info("Done!!!")
            else:
                raise Exception("No official lineup...")    
        except Exception:
            players_data = requests.get(f"http://2.ds.lsapp.eu/pq_graphql?_hash={predicted_lineup}&eventId={match_id}&projectId=2").json()

            findbyid = players_data["data"]
            eventpartic = findbyid["findEventById"]
            typename = eventpartic["eventParticipants"]
            open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "w").close
            if len(typename[1]["predictedLineup"]["players"])> 0:
                lineup1 = typename[1]["predictedLineup"]
                lineup1_teamname = typename[1]["name"]
                lineup2 = typename[0]["predictedLineup"]
                lineup2_teamname = typename[0]["name"]
                logger.info("Predicted lineup Found !!! ")
                players1 = lineup1["players"]
                players2 = lineup2["players"]
                output_header = True
                team1_width =  len(max(players1, key=lambda x: len(x["fieldName"]))["fieldName"])
                team2_width =  len(max(players2, key=lambda x: len(x["fieldName"]))["fieldName"])
                if output_header:
                    with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "w", encoding="utf-8")as writeit:
                        writeit.write(
                            '```\nترکیب احتمالی\n\n\n'                        
                            f'{lineup1_teamname:<{team2_width}}'.ljust(20, " ")+                          
                            f'{lineup2_teamname:<{team1_width}}\n\n'.rjust(20, " ")  
                                        )
                    output_header = False
                with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "a", encoding="utf-8")as writeit:
                    # name_width_team1 = max(len())
                    for i1, i2 in zip(players1, players2):
                        writeit.write(
                            f'{i1["number"]:>2} {i1["fieldName"]:<{team1_width}}'                            f'     {i2["fieldName"]:<{team2_width}} {i2["number"]:>2}\n'.rjust(20,"-")
                            
                                        )
                    writeit.write("```")
                logger.info("DONE !") 
            else:
                logger.info("No lineup found...")
                
if __name__ == "__main__":
    main_function("ars")