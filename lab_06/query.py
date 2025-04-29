# 1. Скалярный запрос
def scalar_query(cursor):
    print("Вывести количество животных в таблице, возраст которых больше 6")
    cursor.execute("SELECT COUNT(*) AS total_animals FROM animals_json where age > 6;")
    result = cursor.fetchone()
    print(f"Всего животных старше 6 лет: {result['total_animals']}")


# 2. Запрос с несколькими соединениями (JOIN)
def join_query(cursor):
    print("Вывести животное и зону в которой оно живет")
    cursor.execute("""
        SELECT a.name AS animal_name, e.location AS enclosure_location
        FROM animals_json a
        JOIN enclosures e ON a.enclosure_id = e.id;
    """)
    for row in cursor.fetchall():
        print(f"Animal: {row['animal_name']}, Enclosure: {row['enclosure_location']}")


# 3. Запрос с ОТВ (CTE) и оконными функциями
def cte_window_query(cursor):
    print("Вывести работника, руководителя и ранжирование по возрасту")
    cursor.execute("""
    WITH staff_with_managers AS (
    SELECT 
        s.id AS employee_id,
        s.name AS employee_name,
        s.age AS employee_age,
        m.name AS manager_name
    FROM 
        staff_r s
    LEFT JOIN 
        staff_r m ON s.manager_id = m.id
)
SELECT 
    employee_id,
    employee_name,
    employee_age,
    manager_name,
    RANK() OVER (ORDER BY employee_age DESC) AS age_rank
FROM 
    staff_with_managers;
    """)
    for row in cursor.fetchall():
        print(
            f"Имя: {row['employee_name']}, Руководитель: {row['manager_name']}, Ранжирование по возрасту: {row['age_rank']}")


# 4. Запрос к метаданным
def metadata_query(cursor):
    print("Вывести все таблицы из схемы public")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    for row in cursor.fetchall():
        print(f"Table: {row['table_name']}")


# 5. Вызов скалярной функции
def call_scalar_function(cursor):
    print("Вывести время с момента последнего ухода")
    cursor.execute("""
    select a.name, a.species, c.care_date, calculate_passing_time(c.care_date) as time_after_care
    from care c
    join animals a on a.id = c.animal_id;
    """)
    result = cursor.fetchone()
    print(
        f"Животное: {result['name']}, {result['species']} Время с момента последнего ухода: {result['time_after_care']}")


# 6. Вызов табличной функции
def call_table_function(cursor):
    print("Вывести всех животных в загоне 24")
    cursor.execute("SELECT * FROM get_animals_in_enclosure(24);")
    for row in cursor.fetchall():
        print(row)


# 7. Вызов хранимой процедуры
def call_procedure(cursor):
    print("Вывести количество животных в таблице")
    cursor.execute("CALL get_animal_count();")
    cursor.execute("SELECT animal_count FROM temp_result;")
    animal_count = cursor.fetchone()
    print("Суммарно животных в таблице: ", animal_count['animal_count'])


# 8. Вызов системной функции
def call_system_function(cursor):
    cursor.execute("SELECT version();")
    result = cursor.fetchone()
    print(f"Версия postgreSQL: {result['version']}")


# 9. Создание таблицы
def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feeding_schedule (
            id SERIAL PRIMARY KEY,
            animal_id INT REFERENCES animals_json(id),
            feed_time TEXT,
            food_type TEXT
        );
    """)
    print("Table 'feeding_schedule' created successfully.")


# 10. Вставка данных
def insert_data(cursor):
    cursor.execute("""
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
          AND table_name = 'feeding_schedule'
    );
""")
    table_exists = cursor.fetchone()['exists']

    if table_exists:
        cursor.execute("""
            INSERT INTO feeding_schedule (animal_id, feed_time, food_type)
            VALUES (1, '08:00', 'Meat'), (2, '10:00', 'Grass');
        """)

        cursor.execute("""
                    select * from feeding_schedule
                """)
    else:
        print("Таблица не существует")
