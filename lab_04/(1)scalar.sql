-- Функция для получения подробной информации о животном, загоне и сотрудниках

create or replace function get_animal_details(animal_id int)
returns text
language plpython3u
as $$
animal_details = plpy.execute(f"""
    select a.name as animal_name, a.species, a.age, a.gender, e.location as enclosure_location, 
           s.name as staff_name, c.care_date 
    from animals a
    join enclosures e on a.enclosure_id = e.id
    left join care c on a.id = c.animal_id
    left join staff s on c.staff_id = s.id
    where a.id = {animal_id};
""")

if animal_details:
    details = animal_details[0]
    result = f"Name: {details['animal_name']}, Species: {details['species']}, Age: {details['age']}, " \
             f"Gender: {details['gender']}, Enclosure: {details['enclosure_location']}, " \
             f"Care given by: {details['staff_name']} on {details['care_date']}"
    return result
else:
    return "Animal not found"
$$;

select get_animal_details(5);