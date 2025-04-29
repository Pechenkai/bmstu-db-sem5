create table animal_insert_log (
    log_id SERIAL primary key,
    animal_id int,
    name varchar(50),
    insertion_time timestamp default current_timestamp
);

create or replace function log_animal_insertion()
returns trigger as $$
begin
    insert into animal_insert_log (animal_id, name)
    values (new.id, new.name);
    
    return new;
end;
$$ language plpgsql;

create trigger after_animal_insert
after insert on animals
for each row
execute function log_animal_insertion();