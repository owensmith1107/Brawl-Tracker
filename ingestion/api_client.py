import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BRAWL_API_KEY")
BASE_URL = "https://api.brawlstars.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

def format_tag(tag: str) -> str:
    """The API requires tags without '#' and URL-encoded with %23"""
    return tag.strip().lstrip("#")

def get_player(player_tag: str) -> dict:
    tag = format_tag(player_tag)
    response = requests.get(f"{BASE_URL}/players/%23{tag}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_battle_log(player_tag: str) -> list:
    tag = format_tag(player_tag)
    response = requests.get(f"{BASE_URL}/players/%23{tag}/battlelog", headers=HEADERS)
    response.raise_for_status()
    return response.json().get("items", [])