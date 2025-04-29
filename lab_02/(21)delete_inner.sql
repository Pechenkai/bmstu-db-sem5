delete from animals
where enclosure_id IN (
    select e.id
    from enclosures e
    where e.type = 'BigCat' and e.id = animals.enclosure_id
);