with CTE as (
    select *,
           ROW_NUMBER() over (partition by name, species, type, age, gender, enclosure_id order by id) as rn
    from animals
)

delete from animals
where id in (select id from CTE where rn > 1)