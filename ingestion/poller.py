import os
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ingestion.api_client import get_battle_log
from db.models import Battle, BattlePlayer, get_engine

load_dotenv()

PLAYER_TAG = os.getenv("PLAYER_TAG")


def generate_battle_id(battle_time: str, player_tag: str) -> str:
    """Generate a unique ID from the battle time + your player tag."""
    raw = f"{battle_time}_{player_tag}"
    return hashlib.md5(raw.encode()).hexdigest()


def parse_battle_time(battle_time: str) -> datetime:
    """Convert '20260304T172518.000Z' to a Python datetime."""
    return datetime.strptime(battle_time, "%Y%m%dT%H%M%S.%fZ")


def find_my_team(teams: list, player_tag: str) -> int:
    """Return 0 or 1 depending on which team the player is on."""
    clean_tag = player_tag.strip().lstrip("#")
    for i, team in enumerate(teams):
        for player in team:
            if player["tag"].lstrip("#") == clean_tag:
                return i
    return -1  # shouldn't happen


def poll(player_tag: str = PLAYER_TAG):
    engine = get_engine()
    battles = get_battle_log(player_tag)
    clean_tag = player_tag.strip().lstrip("#")

    new_count = 0
    skipped_count = 0

    with Session(engine) as session:
        for raw in battles:
            battle_time_str = raw["battleTime"]
            battle_id = generate_battle_id(battle_time_str, clean_tag)

            # Deduplication check — skip if we've already stored this battle
            existing = session.get(Battle, battle_id)
            if existing:
                skipped_count += 1
                continue

            event = raw.get("event", {})
            battle = raw.get("battle", {})
            teams = battle.get("teams", [])
            star_player = battle.get("starPlayer", {})
            my_team_index = find_my_team(teams, player_tag)

            new_battle = Battle(
                id=battle_id,
                battle_time=parse_battle_time(battle_time_str),
                event_id=event.get("id"),
                event_mode=event.get("mode"),
                map_name=event.get("map"),
                battle_mode=battle.get("mode"),
                battle_type=battle.get("type"),
                result=battle.get("result"),
                duration=battle.get("duration"),
                trophy_change=battle.get("trophyChange"),
                star_player_tag=star_player.get("tag", "").lstrip("#") if star_player else None,
            )
            session.add(new_battle)

            # Insert all players from both teams
            for team_index, team in enumerate(teams):
                for player in team:
                    is_self = player["tag"].lstrip("#") == clean_tag
                    bp = BattlePlayer(
                        battle_id=battle_id,
                        player_tag=player["tag"].lstrip("#"),
                        player_name=player.get("name"),
                        team=team_index,
                        is_self=is_self,
                        brawler_id=player["brawler"]["id"],
                        brawler_name=player["brawler"]["name"],
                        brawler_power=player["brawler"]["power"],
                        brawler_trophies=player["brawler"]["trophies"],
                    )
                    session.add(bp)

            new_count += 1

        session.commit()

    print(f"Done. {new_count} new battles inserted, {skipped_count} already existed.")


if __name__ == "__main__":
    poll()