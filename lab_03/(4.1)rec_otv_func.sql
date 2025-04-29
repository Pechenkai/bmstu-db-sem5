--drop function get_subordinates;

--Функция ищет подчиненных данного сотрудника

create or replace function get_subordinates(emp_id int)
returns table (
    id int,
    name varchar,
    "position" varchar,
    age int,
    hire_date date,
    manage_id int
) as $$
begin
    return QUERY
    with recursive subordinates as (
        select *
        from staff_r
        where manager_id = emp_id
        
        union all
        
        select s.*
        from staff_r s
        join subordinates sub on s.manager_id = sub.id
    )
    select * from subordinates;
end;
$$ language plpgsql;