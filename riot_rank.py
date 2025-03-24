import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('My_Secret')
REGION = "KR"  # 한국 서버(KR)
REGION_2 = "asia"

def get_ranked_players(queue="RANKED_SOLO_5x5", tier="PLATINUM", division="I", page=1):
    url = f"https://{REGION}.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page={page}"
    headers = {"X-Riot-Token": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        players = response.json()
        return players
    else:
        return f"Error {response.status_code}: {response.json()}"
    
def get_game_name_by_puuid(puuid):
    url = f"https://{REGION_2}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        game_name = data.get("gameName")
        tag_line = data.get("tagLine")
        return f"{game_name}#{tag_line}"
    else:
        return f"Error {response.status_code}: {response.json()}"


ranked_players = get_ranked_players()

if isinstance(ranked_players, list):
    for i, player in enumerate(ranked_players[:100], 1): # 출력할 개수수
        print(f"{i}. {get_game_name_by_puuid(player['puuid'])} - {player['leaguePoints']} LP - {player['wins']}승 {player['losses']}패")
else:
    print(ranked_players)

