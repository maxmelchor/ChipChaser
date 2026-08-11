import json
import urllib.request

SLEEPER_API = "https://api.sleeper.app/v1/players/nfl"
OUTPUT_FILE = "players.json"

# Positional scarcity defaults
SCARCITY = {"QB": 1.15, "RB": 1.25, "WR": 1.10, "TE": 1.20}

def fetch_and_update():
    print("Fetching Sleeper NFL player database...")
    req = urllib.request.Request(SLEEPER_API, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())

    # Try to keep existing custom values if players.json exists
    existing_data = {}
    try:
        with open(OUTPUT_FILE, "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        pass

    updated_players = {}

    for player_id, p in data.items():
        pos = p.get("position")
        full_name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip().lower()

        if full_name and pos in ["QB", "RB", "WR", "TE"]:
            # If already customized in players.json, preserve values
            if full_name in existing_data:
                updated_players[full_name] = existing_data[full_name]
                # Update injury penalty if status changed
                updated_players[full_name]["injury"] = -10 if p.get("injury_status") else 0
            else:
                # Generate new baseline entry for newly discovered players/rookies
                updated_players[full_name] = {
                    "baseValue": 65,
                    "scarcity": SCARCITY.get(pos, 1.0),
                    "ros": 0,
                    "injury": -10 if p.get("injury_status") else 0,
                    "contingency": 8
                }

    # Write updated payload back to players.json
    with open(OUTPUT_FILE, "w") as f:
        json.dump(updated_players, f, indent=2)

    print(f"Successfully updated {len(updated_players)} players in {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_update()
