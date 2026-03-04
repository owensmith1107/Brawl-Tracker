with enriched as (
    select * from {{ ref('int_battle_players_enriched') }}
),

-- Get just my battles and which team I was on
my_battles as (
    select
        battle_id,
        team        as my_team,
        result
    from enriched
    where is_self = true
),

-- Get all teammates (same battle, same team, not me)
teammates as (
    select
        e.player_tag        as teammate_tag,
        e.player_name       as teammate_name,
        e.brawler_name      as teammate_brawler,
        m.result
    from enriched e
    join my_battles m
        on e.battle_id = m.battle_id
        and e.team = m.my_team
    where e.is_self = false
),

stats as (
    select
        teammate_tag,
        teammate_name,
        count(*)                                                    as games_together,
        sum(case when result = 'victory' then 1 else 0 end)        as wins,
        round(
            sum(case when result = 'victory' then 1 else 0 end)
            * 100.0 / count(*), 1
        )                                                           as win_rate_pct
    from teammates
    group by teammate_tag, teammate_name
)

select * from stats
order by games_together desc