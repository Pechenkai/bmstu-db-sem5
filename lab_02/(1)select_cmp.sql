SELECT a.name, a.age, a.species, e.color, e.type
FROM animals a
JOIN enclosures e ON a.enclosure_id = e.id
WHERE a.age >= 5 AND e.type = 'Primate'