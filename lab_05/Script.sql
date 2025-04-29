copy (select array_to_json(array_agg(row_to_json(a))) from animals as a)
to '/tmp/animals.json';

select row_to_json(a) from animals as a;

copy (select array_to_json(array_agg(row_to_json(e))) from enclosures as e)
to '/tmp/enclosures.json';

select row_to_json(e) from enclosures as e;

copy (select array_to_json(array_agg(row_to_json(s))) from staff as s)
to '/tmp/staff.json';

select row_to_json(s) from staff as s;

copy (select array_to_json(array_agg(row_to_json(c))) from care as c)
to '/tmp/care.json';

select row_to_json(c) from care as c;

drop table if exists animals_json;

create table if not exists animals_json (
    id serial primary key,
    name text,
    species text,
    type text,
    age int,
    gender char(1),
    enclosure_id int,
    constraint fk_ae foreign key (enclosure_id) references enclosures(id),
    constraint age_val check (age > 0),
    constraint gen_val check (gender in ('M', 'F'))  
);

drop table if exists tmp_json;

create temp table if not exists tmp_json
(
    data jsonb
);


copy tmp_json(data) from '/tmp/animals.json';

SELECT data, jsonb_typeof(data) AS data_type
FROM tmp_json;

select * from tmp_json;

insert into animals_json (name, species, type, age, gender, enclosure_id)
select
    obj->>'name',
    obj->>'species',
    obj->>'type',
    (obj->>'age')::int,
    obj->>'gender',
    (obj->>'enclosure_id')::int
from (
    select jsonb_array_elements(data) as obj
    from tmp_json
) as expanded
where jsonb_typeof(obj) = 'object';


select * from animals_json

create table medical_records (
    id serial primary key,
    animal_id int references animals_json(id),
    medical_history jsonb
);

insert into medical_records (animal_id, medical_history)
values
(1, '{"visits": [{"date": "2023-03-01", "reason": "routine checkup"}, {"date": "2024-02-15", "reason": "dental cleaning"}]}'),
(2, '{"visits": [{"date": "2024-05-20", "reason": "injury treatment"}, {"date": "2024-07-10", "reason": "follow-up"}]}'),
(3, '{"visits": [{"date": "2023-12-01", "reason": "vaccination"}, {"date": "2024-06-14", "reason": "nutritional consultation"}]}'),
(4, '{"visits": [{"date": "2023-08-23", "reason": "deworming"}, {"date": "2024-03-12", "reason": "general health evaluation"}]}'),
(5, '{"visits": [{"date": "2024-04-05", "reason": "injury assessment"}, {"date": "2024-09-30", "reason": "fracture treatment"}]}'),
(6, '{"visits": [{"date": "2024-01-20", "reason": "eye infection treatment"}, {"date": "2024-05-01", "reason": "skin allergy treatment"}]}'),
(7, '{"visits": [{"date": "2023-11-12", "reason": "vaccination"}, {"date": "2024-08-22", "reason": "blood test"}]}'),
(8, '{"visits": [{"date": "2024-02-11", "reason": "dental cleaning"}, {"date": "2024-03-27", "reason": "arthritis check"}]}'),
(9, '{"visits": [{"date": "2023-10-15", "reason": "nutrition adjustment"}, {"date": "2024-06-20", "reason": "follow-up consultation"}]}'),
(10, '{"visits": [{"date": "2023-12-20", "reason": "skin allergy treatment"}, {"date": "2024-02-10", "reason": "nutrition consultation"}]}');

select * from medical_records;

select medical_history->'visits' as visits
from medical_records
where animal_id = 1;

select (medical_history->'visits'->0->>'reason') as first_visit_reason
from medical_records
where animal_id = 1;

select (medical_history->'visits'->0->>'date')::date as first_visit_reason
from medical_records
where animal_id = 1;

select animal_id, medical_history ? 'visits' as has_visits
from medical_records;

update medical_records
set medical_history = jsonb_set(
    medical_history,
    '{last_updated}',
    to_jsonb(now()::text)
)
where animal_id = 1;

select 
    animal_id,
    visit->>'date' as visit_date,
    visit->>'reason' as visit_reason
from (
    select animal_id, jsonb_array_elements(medical_history->'visits') as visit
    from medical_records
) as visits_expanded;

