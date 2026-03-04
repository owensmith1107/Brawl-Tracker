with source as (
    select * from {{ source('public', 'battle_players') }}
),

renamed as (
    select
        id              as battle_player_id,
        battle_id,
        player_tag,
        player_name,
        team,
        is_self,
        brawler_id,
        brawler_name,
        brawler_power,
        brawler_trophies
    from source
)

select * from renamed