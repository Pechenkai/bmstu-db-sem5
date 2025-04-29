--Подсчитать количество животных в загоне каждой локации.

select e.location,
       e.type,
       COUNT(a.id) as total_animals
from enclosures e
join animals a on e.id = a.enclosure_id
group by e.location, e.type
order by e.location