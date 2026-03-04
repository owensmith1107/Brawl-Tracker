with source as (
    select * from {{ source('public', 'battles') }}
),

renamed as (
    select
        id                                      as battle_id,
        battle_time,
        event_id,
        event_mode,
        map_name,
        battle_mode,

        -- Translate API's confusing type names to meaningful labels
        case battle_type
            when 'ranked'       then 'trophy_road'
            when 'soloRanked'   then 'ranked_solo'
            when 'teamRanked'   then 'ranked_team'
            when 'friendly'     then 'friendly'
            else battle_type
        end                                     as game_type,

        result,
        duration,
        trophy_change,
        star_player_tag
    from source
)

select * from renamed