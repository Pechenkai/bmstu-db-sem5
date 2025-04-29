--drop function get_animals_in_enclosure;

--Функция возвращает животных в данном загоне.

create or replace function get_animals_in_enclosure(enclosure_id_param INT)
returns table (animal_id int, name text, species text, age int) as $$
begin
    return QUERY
    select a.id, a.name, a.species, a.age
    from animals a
    where a.enclosure_id = enclosure_id_param;
end;
$$ language plpgsql;