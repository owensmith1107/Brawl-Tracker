with my_battles as (
    select * from {{ ref('int_battle_players_enriched') }}
    where is_self = true
),

stats as (
    select
        map_name,
        event_mode,
        game_type,
        count(*)                                                    as games_played,
        sum(case when result = 'victory' then 1 else 0 end)        as wins,
        sum(case when result = 'defeat' then 1 else 0 end)         as losses,
        round(
            sum(case when result = 'victory' then 1 else 0 end)
            * 100.0 / count(*), 1
        )                                                           as win_rate_pct,
        avg(trophy_change)                                          as avg_trophy_change
    from my_battles
    group by map_name, event_mode, game_type
)

select * from stats
order by games_played desc