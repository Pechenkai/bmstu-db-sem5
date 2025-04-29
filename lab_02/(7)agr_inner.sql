select e."location", e."type", count(e.id), avg(a.age)
from enclosures e 
join animals a on e.id = a.id 
group by e."location", e.type 
order by e."location"