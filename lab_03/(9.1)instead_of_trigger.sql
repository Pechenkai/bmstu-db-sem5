create view animals_view as
select * from animals;

create or replace function soft_delete_animal()
returns trigger as $$
begin
    update animals
    set is_deleted = true
    where id = old.id;
    
    return null;
end;
$$ language plpgsql;

create trigger instead_of_animal_delete
instead of delete on animals_view
for each row
execute function soft_delete_animal();

delete from animals_view where id = 2223