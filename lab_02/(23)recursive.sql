drop table if exists staff_r; 

create table staff_r (
    id SERIAL primary key,
    name varchar(50) not null,
    position varchar(50) not null,
    age int not null,
    hire_date date not null,
    manager_id int null,
    constraint fk_manager foreign key (manager_id) references staff_r(id) on delete set null
);

insert into staff_r (name, position, age, hire_date, manager_id)
values 
('Иван', 'Директор', 45, '2010-01-01', NULL),
('Анна', 'Заместитель директора', 40, '2015-02-01', 1),
('Сергей', 'Менеджер', 35, '2018-03-01', 2),
('Ольга', 'Секретарь', 30, '2019-04-01', 2),
('Дмитрий', 'Ведущий специалист', 28, '2020-05-01', 3);

with recursive RecursiveStaff as (
    select 
        id as EmployeeID,
        name as EmployeeName,
        position as Title,
        manager_id,
        0 as Level
    from staff_r
    where manager_id IS NULL
    
    union all
    
    select 
        s.id as EmployeeID,
        s.name as EmployeeName,
        s.position as Title,
        s.manager_id,
        Level + 1
    from staff_r as s
    inner join RecursiveStaff as rs on s.manager_id = rs.EmployeeID
)

select 
    EmployeeID, 
    EmployeeName, 
    Title, 
    manager_id, 
    Level
from RecursiveStaff
order by Level, EmployeeName;