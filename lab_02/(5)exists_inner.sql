--Найти всех сотрудников, которые ухаживали за животными, старше 10 лет.

select s."name", s."position" 
from staff s 
where exists (select 1 
from care c
join animals a on c.animal_id = a.id 
where c.staff_id = s.id and a.age > 10)
