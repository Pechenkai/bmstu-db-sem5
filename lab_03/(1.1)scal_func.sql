--Функция считает время, пройденное с данной даты в годах и месяцах

create or replace function calculate_passing_time(birth_date date)
returns text as $$
declare
    years int;
    months int;
begin
    years := extract(year from age(current_date, birth_date));
    months := extract(month from age(current_date, birth_date));
    return years || ' years and ' || months || ' months';
end;
$$ language plpgsql;
