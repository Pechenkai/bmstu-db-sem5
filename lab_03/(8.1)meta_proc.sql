create or replace procedure list_tables()
language plpgsql
as $$
declare
    table_record record;
begin
    for table_record in
        select table_name
        from information_schema.tables
        where table_schema = 'public'
    loop
        raise notice 'Table: %', table_record.table_name;
    end loop;
end;
$$;