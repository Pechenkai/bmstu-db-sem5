Querry1 = """
select *
from satellite s 
where s.country = 'Россия'
order by date 
limit 1;
"""

Querry2 = """
select s.id, s.name
from satellite s
left join flight f 
    on s.id = f.sat_id 
    and f.type = 0 
    and date_trunc('year', f.date) = date_trunc('year', CURRENT_DATE)
where f.id is null;
"""

Querry3 = """
select s.id, s.name
from satellite s
join flight f 
    on s.id = f.sat_id
where f.type = 0
  and f.date between '2024-01-01'::date and '2024-01-11'::date
 group by s.id;
"""