--Процедура выводит животных

create or replace procedure list_animals()
language plpgsql
as $$
declare
    animal_cursor cursor for select name, species, age from animals;
    animal_record RECORD;
begin
    open animal_cursor;
    loop
        fetch animal_cursor into animal_record;
        exit when not found;
        raise notice 'Name: %, Species: %, Age: %', animal_record.name, animal_record.species, animal_record.age;
    end loop;
    close animal_cursor;
end;
$$;