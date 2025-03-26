import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('My_Secret')
PUUID = "WzJ8DGCkUEE2YohFntdDbhcK3uHxqovUPib6OxuwkWgR9YL_wjuVaoXotDFxBGAfgv5w6TYla48Ucg"
REGION = "kr"

url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{PUUID}"

headers = {
    "X-Riot-Token": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    revision_date = data.get("revisionDate") 
    rev_date_utc = datetime.utcfromtimestamp(revision_date / 1000)
    time_passed = datetime.utcnow() - rev_date_utc

    summoner_level = data.get("summonerLevel")  

    print(f"Current Date (Unix Timestamp): {datetime.utcnow()}")
    print(f"Revision Date (Unix Timestamp): {rev_date_utc}")
    print(f"Time passed (Unix Timestamp): {time_passed}")
    print(f"Summoner Level: {summoner_level}")
else:
    print(f"Error: {response.status_code} - {response.text}")
