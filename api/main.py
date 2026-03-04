from fastapi import FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.models import get_engine
from typing import Optional

app = FastAPI(
    title="BrawlTracker API",
    description="Personal Brawl Stars stats API",
    version="1.0.0"
)

engine = get_engine()


def query(sql: str, params: dict = {}) -> list[dict]:
    with Session(engine) as session:
        result = session.execute(text(sql), params)
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]


@app.get("/")
def root():
    return {"status": "ok", "message": "BrawlTracker API is running"}


@app.get("/stats/brawlers")
def brawler_stats(game_type: Optional[str] = Query(None)):
    sql = """
        select * from analytics.mart_brawler_stats
        where (:game_type is null or game_type = :game_type)
        order by games_played desc
    """
    return query(sql, {"game_type": game_type})


@app.get("/stats/maps")
def map_stats(
    game_type: Optional[str] = Query(None),
    mode: Optional[str] = Query(None)
):
    sql = """
        select * from analytics.mart_map_stats
        where (:game_type is null or game_type = :game_type)
        and (:mode is null or event_mode = :mode)
        order by games_played desc
    """
    return query(sql, {"game_type": game_type, "mode": mode})


@app.get("/stats/teammates")
def teammate_stats(min_games: int = Query(1)):
    sql = """
        select * from analytics.mart_teammate_stats
        where games_together >= :min_games
        order by games_together desc
    """
    return query(sql, {"min_games": min_games})


@app.get("/battles")
def battles(
    game_type: Optional[str] = Query(None),
    map_name: Optional[str] = Query(None),
    limit: int = Query(50)
):
    sql = """
        select * from analytics.stg_battles
        where (:game_type is null or game_type = :game_type)
        and (:map_name is null or map_name = :map_name)
        order by battle_time desc
        limit :limit
    """
    return query(sql, {"game_type": game_type, "map_name": map_name, "limit": limit})