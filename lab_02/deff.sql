-- Вывести всех сотрудников ухаживающих за животными мужского пола

select distinct s."name" as s_name, s."position" as s_position, a."name" as a_name, a.gender as a_gender
from care c
join staff s on s.id = c.staff_id 
join animals a on a.id = c.animal_id 
where a.gender = 'M'
