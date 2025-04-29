--Для каждого животного вывести его имя, вид, возраст и имя сотрудника, который ухаживал за ним больше всего раз.

select a."name", a.species, a.age, (select s.name
from staff s
join care c on s.id = c.staff_id
where c.animal_id = a.id 
group by s.name
order by count(*) desc
limit 1) as most_care_staff
from animals a