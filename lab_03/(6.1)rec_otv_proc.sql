--drop procedure get_sub(man_id int);

--Процедура выводит всех подчиненных данного сотрудника

create or replace procedure get_sub(man_id int)
language plpgsql
as $$
declare
    emp_record RECORD;
begin
    create temp table temp_subordinates (
        id int,
        name varchar(50),
        position varchar(50)
    );

    with recursive subordinates as (
        select id, name, position from staff_r where manager_id = $1
        union all
        select s.id, s.name, s.position from staff_r s
        inner join subordinates st on s.manager_id = st.id
    )
    insert into temp_subordinates
    select * from subordinates;

    for emp_record in select * from temp_subordinates loop
        raise notice 'ID: %, Name: %, Position: %', emp_record.id, emp_record.name, emp_record.position;
    end loop;

    drop table temp_subordinates;
end;
$$;