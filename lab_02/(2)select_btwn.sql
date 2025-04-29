select s.name, s.id, s.position, c.care_date, c.id 
from care c
join staff s on c.staff_id = s.id 
where c.care_date between '2023-02-01' and '2023-03-01'
