--Найти животных, которые старше хотя бы одного животного типа 'SmallBird'.

select id, name, species, age
from animals
where age > any(select age 
from animals a
join enclosures e on e.id = a.enclosure_id
where a.type = 'SmallBird')