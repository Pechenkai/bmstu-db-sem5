CREATE OR REPLACE FUNCTION get_animals_in_enclosure_with_avg_age(enclosure_id_param int)
RETURNS TABLE(animal_id int, animal_name text, animal_age int, average_age float) AS $$
    query = f"""
        select id, name, age
        from animals
        where enclosure_id = {enclosure_id_param}
    """
    
    animals_data = plpy.execute(query)
    
    total_age = 0
    total_count = len(animals_data)
    
    for animal in animals_data:
        total_age += animal['age']
    
    if total_count > 0:
        average_age = total_age / total_count
    else:
        average_age = 0
    
    result = []
    for animal in animals_data:
        result.append((animal['id'], animal['name'], animal['age'], average_age))
    
    return result
$$ language plpython3u;

select * from get_animals_in_enclosure_with_avg_age(4);