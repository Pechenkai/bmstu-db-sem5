create temporary table temp_care as
select a.name as animal_name,
       c.care_date,
       s.name as staff_name
from care c
join animals a on c.animal_id = a.id
join staff s on c.staff_id = s.id;

select * from temp_care