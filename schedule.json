import json
import urllib.request

def fetch_and_save_nfl_schedule(season_year=2026):
    print("Fetching complete NFL schedule from ESPN API...")
    full_schedule = {}

    for week in range(1, 19):
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={season_year}&week={week}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                week_games = []
                
                for event in data.get("events", []):
                    competition = event["competitions"][0]
                    competitors = competition["competitors"]
                    
                    home_team = next(c["team"]["abbreviation"] for c in competitors if c["homeAway"] == "home")
                    away_team = next(c["team"]["abbreviation"] for c in competitors if c["homeAway"] == "away")
                    
                    week_games.append({"home": home_team, "away": away_team})
                
                full_schedule[f"week_{week}"] = week_games
        except Exception as e:
            print(f"Error fetching Week {week}: {e}")

    with open("schedule.json", "w") as f:
        json.dump(full_schedule, f, indent=2)
    print("Successfully generated schedule.json!")

if __name__ == "__main__":
    fetch_and_save_nfl_schedule(2026)
