import os
import json
from dotenv import load_dotenv
from ingestion.api_client import get_battle_log

load_dotenv()

PLAYER_TAG = os.getenv("PLAYER_TAG")

battles = get_battle_log(PLAYER_TAG)
print(json.dumps(battles[0], indent=2))

