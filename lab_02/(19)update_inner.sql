--Обновление возраста животного на основе среднего возраста всех животных того же вида (Lion)

update animals
set age = (select avg(age) from animals where species = animals.species)
where species = 'Lion';