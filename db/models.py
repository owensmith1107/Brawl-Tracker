from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Battle(Base):
    __tablename__ = "battles"

    id = Column(String, primary_key=True)  # we'll generate this from battleTime + player tag
    battle_time = Column(DateTime, nullable=False)
    event_id = Column(Integer)
    event_mode = Column(String)
    map_name = Column(String)
    battle_mode = Column(String)
    battle_type = Column(String)  # "ranked", "friendly", "soloRanked", etc.
    result = Column(String)       # "victory", "defeat", "draw"
    duration = Column(Integer)
    trophy_change = Column(Integer)
    star_player_tag = Column(String)

    players = relationship("BattlePlayer", back_populates="battle")


class BattlePlayer(Base):
    __tablename__ = "battle_players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    battle_id = Column(String, ForeignKey("battles.id"), nullable=False)
    player_tag = Column(String, nullable=False)
    player_name = Column(String)
    team = Column(Integer)        # 0 or 1 — which team they were on
    is_self = Column(Boolean)     # True if this is your own account
    brawler_id = Column(Integer)
    brawler_name = Column(String)
    brawler_power = Column(Integer)
    brawler_trophies = Column(Integer)

    battle = relationship("Battle", back_populates="players")


def get_engine():
    return create_engine(os.getenv("DB_URL"))


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()