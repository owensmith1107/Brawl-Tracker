with battles as (
    select * from {{ ref('stg_battles') }}
),

players as (
    select * from {{ ref('stg_battle_players') }}
),

enriched as (
    select
        p.battle_player_id,
        p.battle_id,
        p.player_tag,
        p.player_name,
        p.team,
        p.is_self,
        p.brawler_id,
        p.brawler_name,
        p.brawler_power,
        p.brawler_trophies,

        -- Battle context on every player row
        b.battle_time,
        b.map_name,
        b.event_mode,
        b.game_type,
        b.result,
        b.duration,
        b.trophy_change,
        b.star_player_tag,

        -- Derived fields
        case when p.is_self then b.result else null end  as my_result,
        case when p.player_tag = b.star_player_tag
             then true else false end                    as was_star_player,
        case when p.is_self and p.team = 0 then 1
             when p.is_self and p.team = 1 then 1
             else 0 end                                  as my_team_index

    from players p
    join battles b on p.battle_id = b.battle_id
)

select * from enriched