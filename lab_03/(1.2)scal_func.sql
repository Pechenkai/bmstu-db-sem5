select a.name, a.species, c.care_date, calculate_passing_time(c.care_date) as time_after_care
from care c
join animals a on a.id = c.animal_id 