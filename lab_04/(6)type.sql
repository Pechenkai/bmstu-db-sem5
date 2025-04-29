create type animal_care_info as (
    animal_id int,
    staff_id int,
    care_date date,
    description text
);

create or replace function get_animal_care_info(animal_id int)
returns animal_care_info
language plpython3u
as $$
result = plpy.execute(f"""
    select animal_id, staff_id, care_date, description
    from care
    where animal_id = {animal_id}
    order by care_date desc
    limit 1;
""")

if result:
    return result[0]
else:
    return (animal_id, None, None, 'No care record found')
$$;

select * from get_animal_care_info(5);