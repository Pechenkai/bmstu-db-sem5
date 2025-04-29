--Найти животных, чей возраст больше чем средний возрст животных, находящихся в вольере зклкного цвета

select a.id, a.name as animal_name, a.age
from animals a
where a.age > (
    select avg(a2.age)
    from animals a2
    where a2.enclosure_id in (
        select e.id
        from enclosures e
        where e.color = 'Green'
    )
);