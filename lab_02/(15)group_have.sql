--Подсчитать количество животных в загоне каждой локации и вывести если больше 20.

select e.location,
       e.type,
       count(a.id) as total_animals
from enclosures e
left join animals a on e.id = a.enclosure_id
group by e.location, e.type
having count(a.id) > 20
order by e.location;