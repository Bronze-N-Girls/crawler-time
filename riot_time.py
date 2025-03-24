import requests
import datetime
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('My_Secret')
REGION = "asia"  # 지역에 맞게 변경 (KR 유저라면 "asia" 사용)

def get_summoner_puuid(riot_id):
    id_split = riot_id.split('#')
    summoner_name = id_split[0]
    tag_line = id_split[1]
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    summoner_name_print = response.json().get("gameName")
    tag_line_print = response.json().get("tagLine")
    riot_id_print = summoner_name_print + tag_line_print

    if response.status_code == 200:
        return response.json().get("puuid")
    else:
        return f"Error: {response.status_code}, {response.json()}"

def get_recent_match_id(puuid):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    match_ids = response.json()
    return match_ids[0] if match_ids else None

def convert_utc_to_kst(utc_timestamp):
    """UTC timestamp (밀리초)를 KST (한국 시간)으로 변환"""
    utc_time = datetime.datetime.fromtimestamp(utc_timestamp / 1000, datetime.UTC)  # 밀리초 → 초 변환
    kst_zone = pytz.timezone("Asia/Seoul")
    kst_time = utc_time.astimezone(kst_zone)
    return kst_time

def time_since(kst_time):
    """현재 시간과 주어진 시간(kst_time) 사이의 경과 시간을 반환"""
    now = datetime.datetime.now(pytz.timezone("Asia/Seoul"))  # 현재 한국 시간
    delta = now - kst_time

    days = delta.days
    years, remainder_days = divmod(days, 365)
    months, remainder_days = divmod(remainder_days, 30)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if years > 0:
        return f"{years}년 전"
    elif months > 0:
        return f"{months}개월 전"
    elif days > 0:
        return f"{days}일 전"
    elif hours > 0:
        return f"{hours}시간 전"
    elif minutes > 0:
        return f"{minutes}분 전"
    else:
        return f"{seconds}초 전"

def get_match_date(match_id):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        game_creation = response.json()["info"]["gameCreation"]
        kst_time = convert_utc_to_kst(game_creation)
        elapsed_time = time_since(kst_time)
        return kst_time.strftime('%Y-%m-%d %H:%M:%S'), elapsed_time
    else:
        return f"Error: {response.status_code}, {response.json()}", None

def get_recent_game_date(riot_id):
    puuid = get_summoner_puuid(riot_id)
    if not puuid or "Error" in puuid:
        return "소환사를 찾을 수 없습니다.", None

    match_id = get_recent_match_id(puuid)
    if not match_id:
        return "최근 게임 기록이 없습니다.", None

    return get_match_date(match_id)

# 사용 예시
riot_id = "베이가#7260"  # Riot ID 입력
recent_game_date, elapsed_time = get_recent_game_date(riot_id)

if elapsed_time:
    print(f"{riot_id}의 최근 게임 날짜 (KST): {recent_game_date}")
    print(f"경과 시간: {elapsed_time}")
else:
    print(recent_game_date)