create or replace function capitalize_name()
returns trigger as $$
    name = TD["new"]["name"]

    words = name.split()
    capitalized_words = [word.capitalize() for word in words]

    TD["new"]["name"] = ' '.join(capitalized_words)

    return "Modify"
$$ language plpython3u;

create or replace trigger cap_name_trigger
before insert on staff
for each row 
execute function capitalize_name();

insert into staff ("name", "position", age, hire_date)
values ('alexander osipov', 'Animal Trainer', 42, '2020-06-13')

select * from staff s 
where name = 'Alexander Osipov'