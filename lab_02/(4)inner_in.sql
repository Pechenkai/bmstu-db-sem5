select name, species, age
from animals
where enclosure_id in (select id
from enclosures 
where location = 'Zone_5')