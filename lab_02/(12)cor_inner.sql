--Найти самое старое животное в каждом загоне

select 'Oldest animal' as criteria, a.name as animal_name, a.age, a.enclosure_id, e.type as enclosure_type
from animals a
join enclosures e on a.enclosure_id = e.id
join (
    select enclosure_id, MAX(age) as max_age
    from animals
    group by enclosure_id
) as max_age_animals
on a.enclosure_id = max_age_animals.enclosure_id
and a.age = max_age_animals.max_age
