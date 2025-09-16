import json
import re
import requests

teamid = {'rma': 'W8mj7MDD', 'bar': 'SKbpVP5K', 'atm': 'jaarqpLQ', 'liv': 'lId4TMwf', 'manu': 'ppjDR086', 'manc': 'Wtn9Stg0', 'che': '4fGZN2oK', 'ars': 'hA1Zm19f', 'tot': 'UDg08Ohm', 'psg': 'CjhkPw0k', 'bay': 'nVp0wiqd', 'bvb': 'nP1i5US1', 'int': 'Iw7eKK25', 'mil': '8Sa8HInO', 'juv': 'C06aJvIB', 'nap': '69Dxbc61', 'est': 'KAtu9Aoa', 'prs': 'KzfvmgGd', 'fra': 'QkGeVG1n', 'ger': 'ptQide1O', 'ita': 'hlKvieGH', 'bel': 'GbB957na', 'eng': 'j9N9ZNFA', 'ned': 'WYintcWb', 'por': 'WvJrjFVN', 'arg': 'f9OppQjp', 'bra': 'I9l9aqLq', 'spa': 'bLyo6mco'}
team_fullname = {
    'rma': 'Real Madrid',
    'bar': 'FC Barcelona',
    'atm': 'Atlético Madrid',
    'liv': 'Liverpool',
    'manu': 'Manchester United',
    'manc': 'Manchester City',
    'che': 'Chelsea',
    'ars': 'Arsenal',
    'tot': 'Tottenham Hotspur',
    'psg': 'Paris Saint-Germain',
    'bay': 'Bayern Munich',
    'bvb': 'Borussia Dortmund',
    'int': 'Inter Milan',
    'mil': 'AC Milan',
    'juv': 'Juventus',
    'nap': 'Napoli',
    'est': 'Esteghlal',
    'prs': 'Persepolis',
    'fra': 'France',
    'ger': 'Germany',
    'ita': 'Italy',
    'bel': 'Belgium',
    'eng': 'England',
    'ned': 'Netherlands',
    'por': 'Portugal',
    'arg': 'Argentina',
    'bra': 'Brazil',
    'spa': 'Spain'
}

team_names_flashscore = {
    'rma': 'real-madrid',
    'bar': 'barcelona',
    'atm': 'atl-madrid',
    'liv': 'liverpool',
    'manu': 'manchester-united',
    'manc': 'manchester-city',
    'che': 'chelsea',
    'ars': 'arsenal',
    'tot': 'tottenham',
    'psg': 'psg',   
    'bay': 'bayern-munich',
    'bvb': 'dortmund',
    'int': 'inter',
    'mil': 'ac-milan',
    'juv': 'juventus',
    'nap': 'napoli',
    'est': 'esteghlal',
    'prs': 'persepolis',
    'fra': 'france',
    'ger': 'germany',
    'ita': 'italy',
    'bel': 'belgium',
    'eng': 'england',
    'ned': 'netherlands',
    'por': 'portugal',
    'arg': 'argentina',
    'bra': 'brazil',
    'spa': 'spain'
}
match_id = ""
def prepare_for_search(teamname):
    return teamname.replace(" ", "-").lower()



def main_function(team_kochoolo):
        global match_id
        next_game_data = requests.get(f"https://www.flashscore.com/team/{team_names_flashscore[team_kochoolo]}/{teamid[team_kochoolo]}/").text


        # Escape the team name to handle special regex characters (like . or +)
        pattern = r"(?<=,\s)[A-Z][A-Za-zÀ-ÿ0-9\s.'-]+?\s(?:v|vs\.?|vs)\s[A-Z][A-Za-zÀ-ÿ0-9\s.'-]+?(?=\s+live\b)"

        match = re.search(pattern, next_game_data)
        if match:
            opponent_team = match.group()
            # print(opponent_team)
        opponent_team_cleaned = [item.strip() for item in opponent_team.split(" v ") if item.strip().lower().replace(" ","-") not in team_names_flashscore[team_kochoolo]]
        print(f"Opponent => {opponent_team_cleaned[0]}")

        if opponent_team_cleaned[0] in team_fullname.values():
            print("Opponent is found in database")
            opponent_short_name =  list(team_fullname.keys())[list(team_fullname.values()).index(opponent_team_cleaned[0])]
            game_data = requests.get(f"https://www.flashscore.com/match/football/{team_names_flashscore[opponent_short_name]}-{teamid[opponent_short_name]}/{team_names_flashscore[team_kochoolo]}-{teamid[team_kochoolo]}/").text
            
        else:
            team_kiri = prepare_for_search(opponent_team_cleaned[0])    
            search_data = requests.get(f"https://s.livesport.services/api/v2/search/?q={team_kiri}&lang-id=1&type-ids=1,2,3,4&project-id=2&project-type-id=1").text
            jsoned = json.loads(search_data)
            team_kiri_id = jsoned[0]["id"]
            team_kiri_flashscore_name = jsoned[0]["url"]
            
            game_data = requests.get(f"https://www.flashscore.com/match/football/{team_kiri_flashscore_name}-{team_kiri_id}/{team_names_flashscore[team_kochoolo]}-{teamid[team_kochoolo]}/").text
            # with open("testdata.txt", "w", encoding="utf-8")as test:
            #      test.write(game_data)  
       
       

        pattern = r'"event_id_c":"(.*?)"'

        match = re.search(pattern, game_data)
        if match:
            match_id = match.group().split(":")[1]
            match_id = match_id.replace('"', '')
            print(f"Match-ID Found => {match_id}")
        else:
            print("Can't find any eventID...\n\n")
        predicted_lineup = "dplie"
        lineup = "dlie2"

        try:
            players_data = requests.get(f"http://2.ds.lsapp.eu/pq_graphql?_hash={lineup}&eventId={match_id}&projectId=2").json()
            findbyid = players_data["data"]
            eventpartic = findbyid["findEventById"]
            typename = eventpartic["eventParticipants"]
            if len(typename[1]["Lineup"])> 0:
                lineup1 = typename[1]["Lineup"]
                lineup2 = typename[0]["Lineup"]
                players1 = lineup1["players"]
                players2 = lineup2["players"]
                print("Official lineup Found !!! ")
                output_header = True
                team1_width =  len(max(players1, key=lambda x: len(x["fieldName"]))["fieldName"])
                team2_width =  len(max(players2, key=lambda x: len(x["fieldName"]))["fieldName"])
                if output_header:
                    with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "w", encoding="utf-8")as writeit:
                        writeit.write(
                            '```\nترکیب رسمی\n\n\n'                        
                                        )
                    output_header = False
                with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "a", encoding="utf-8")as writeit:
                    # name_width_team1 = max(len())
                    for i1, i2 in zip(players1, players2):
                        writeit.write(
                            f'{i1["number"]:>2} {i1["fieldName"]:<{team1_width}}'                            f'     {i2["fieldName"]:<{team2_width}} {i2["number"]:>2}\n'.rjust(20," ")
                            
                                        )
                    writeit.write("```")
                print("Done!!!")
            else:
                raise Exception("No Official lineup found...")    
        except Exception:
            players_data = requests.get(f"http://2.ds.lsapp.eu/pq_graphql?_hash={predicted_lineup}&eventId={match_id}&projectId=2").json()
            findbyid = players_data["data"]
            eventpartic = findbyid["findEventById"]
            typename = eventpartic["eventParticipants"]
            lineup1 = typename[1]["predictedLineup"]
            lineup2 = typename[0]["predictedLineup"]
            print("Predicted lineup Found !!! ")
            players1 = lineup1["players"]
            players2 = lineup2["players"]
            # print(players1)
            output_header = True
            team1_width =  len(max(players1, key=lambda x: len(x["fieldName"]))["fieldName"])
            team2_width =  len(max(players2, key=lambda x: len(x["fieldName"]))["fieldName"])
            if output_header:
                with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "w", encoding="utf-8")as writeit:
                    writeit.write(
                        '```\nترکیب احتمالی\n\n\n'                        
                                    )
                output_header = False
            with open(f"teams_data/forlineup/{team_kochoolo}lineup.txt", "a", encoding="utf-8")as writeit:
                # name_width_team1 = max(len())
                for i1, i2 in zip(players1, players2):
                    writeit.write(
                        f'{i1["number"]:>2} {i1["fieldName"]:<{team1_width}}'                            f'     {i2["fieldName"]:<{team2_width}} {i2["number"]:>2}\n'.rjust(20," ")
                        
                                    )
                writeit.write("```")
            print("DONE !") 

if __name__ == "__main__":
    main_function("rma")