CREATE OR REPLACE PROCEDURE get_average_animal_age_in_enclosure(enclosure_id INT)
LANGUAGE plpython3u AS $$
    query = f"""
        SELECT age FROM animals WHERE enclosure_id = {enclosure_id}
    """
    result = plpy.execute(query)

    if len(result) > 0:
        ages = [row['age'] for row in result]
        
        average_age = sum(ages) / len(ages)
        
        plpy.notice(f"Средний возраст животных в загоне {enclosure_id} составляет {average_age:.2f} лет.")
    else:
        plpy.notice(f"В загоне {enclosure_id} нет животных.")
$$;

CREATE OR REPLACE FUNCTION count_animals_per_enclosure()
RETURNS TABLE(enclosure_id INT, animal_count INT) AS $$
BEGIN
    RETURN QUERY
    SELECT animals.enclosure_id, COUNT(*)::int
    FROM animals
    GROUP BY animals.enclosure_id;
END;
$$ LANGUAGE plpgsql;