--Cредний возраст животных по видам, а затем выбрать записи из этой временной таблицы

with average_ages as (
    select species, avg(age) as avg_age
    from animals
    group by species
)

select a.name, a.species, a.age, aa.avg_age
from animals a
join average_ages aa on a.species = aa.species;