insert into animals (id, name, species, type, age, gender, enclosure_id)
select 20001, 'Leon', 'Lion', 'BigCat', 5, 'M', 3
where not exists (
    select 1
    from animals
    where id = 20001
);