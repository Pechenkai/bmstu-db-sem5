--drop function get_enclosure_report;

--Функция выводит сводку о загоне

create or replace function get_enclosure_report(enclosure_id_param int)
returns table (animal_id int, animal_name text, staff_id int, staff_name text, care_date date) as $$
declare
    animal_id_var int;
    staff_id_var int;
begin
	create temp table animals_temp_table (
        id int,
        name text
    ) on commit drop;

	create temp table care_temp_table (
        animal_id int,
        staff_id int,
        staff_name text,
        care_date date
    ) on commit drop;

    insert into animals_temp_table
    select id, name
    from animals
    where enclosure_id = enclosure_id_param;

    for animal_id_var in (select id from animals_temp_table)
    loop
        insert into care_temp_table
        select c.animal_id, s.id as staff_id, s.name as staff_name, c.care_date
        from care c
        join staff s on c.staff_id = s.id
        where c.animal_id = animal_id_var;
    end loop;

    return QUERY
    select a.id as animal_id, a.name as animal_name, ct.staff_id, ct.staff_name, ct.care_date
    from animals_temp_table a
    join care_temp_table ct on a.id = ct.animal_id;
end;
$$ language plpgsql;