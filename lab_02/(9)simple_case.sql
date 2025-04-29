select a.name as animal_name,
       c.care_date,
       case 
           when c.care_date >= date_trunc('month', CURRENT_DATE) then 'Этот месяц'
           when c.care_date >= date_trunc('month', CURRENT_DATE) - interval '1 month' then 'Прошлый месяц'
           when concat('Несколько месяцев назад (', extract (month from c.care_date), ')')
       end as care_month
from care c
join animals a on c.animal_id = a.id
order by c.care_date desc