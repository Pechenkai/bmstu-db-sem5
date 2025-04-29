SELECT 
    species,
    name,
    age,
    MIN(age) OVER (PARTITION BY species) AS min_age,
    MAX(age) OVER (PARTITION BY species) AS max_age,
    AVG(age) OVER (PARTITION BY species) AS avg_age
FROM 
    animals;