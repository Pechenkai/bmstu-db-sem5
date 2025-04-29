select name, age, enclosure_id, case
	when age < 3 then 'молодое'
	when age between 3 and 10 then 'взрослое'
	else 'пожилое'
end as age_category
from animals