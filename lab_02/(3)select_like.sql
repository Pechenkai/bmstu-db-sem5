select a.id , a.name, a.species, e."location", e."size", e."type" 
from animals a
join enclosures e on e.id  = a.enclosure_id
where e.type like '%Bird%'