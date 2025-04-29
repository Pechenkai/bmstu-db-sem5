select name, species, type, age, gender, enclosure_id, COUNT(*) as cnt
from animals
group by name, species, type, age, gender, enclosure_id
