--Процедура считает количество всех животных в таблице animals 

create or replace procedure get_animal_count()
language plpgsql
as $$
declare
    animal_count int;
begin
    select count(*) into animal_count from animals;
	create temp table temp_result (animal_count int);
    insert into temp_result values (animal_count);
    raise notice 'Total number of animals: %', animal_count;
end;
$$;