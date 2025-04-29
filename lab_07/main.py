from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json

from tables import Base
from linqtoobject import get_animals_by_age, get_staff_with_animal_count, get_enclosures_with_animals, \
    get_care_records_with_details, get_animals_without_care_records

from linqtojson import export_animals_to_json, read_animals_from_json, update_animal_in_json, insert_animal_into_json

from linqtosql import single_table_query, multi_table_query, add_animal, update_animal, delete_animal, \
    call_stored_procedure


def display_main_menu():
    print("\n=== Главное меню ===")
    print("1. Выполнить запросы (задание 1)")
    print("2. Работа с JSON (задание 2)")
    print("3. Работа с SQL (задание 3)")
    print("4. Выход")


def display_queries_menu():
    print("\n=== Меню запросов ===")
    print("1. Животные по возрасту")
    print("2. Сотрудники с количеством животных")
    print("3. Загоны с количеством животных")
    print("4. Детали ухода за животными")
    print("5. Животные без записей об уходе")
    print("6. Назад в главное меню")


def display_json_operations_menu():
    print("\n=== Меню операций с JSON ===")
    print("1. Экспорт данных из базы в JSON")
    print("2. Чтение данных из JSON")
    print("3. Обновление записи в JSON")
    print("4. Добавление записи в JSON")
    print("5. Назад в главное меню")


def display_database_operations_menu():
    print("\n=== Меню операций с базой данных ===")
    print("1. Однотабличный запрос")
    print("2. Многотабличный запрос")
    print("3. Добавление данных")
    print("4. Изменение данных")
    print("5. Удаление данных")
    print("6. Вызов хранимой процедуры")
    print("7. Назад в главное меню")


def main():
    DATABASE_URL = "url"
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        while True:
            display_main_menu()
            choice = input("Выберите опцию: ")

            if choice == "1":
                while True:
                    display_queries_menu()
                    query_choice = input("Выберите запрос: ")

                    if query_choice == "1":
                        print("\n=== Животные по возрасту ===")
                        min_age = int(input("Введите минимальный возраст: "))
                        get_animals_by_age(session, min_age)
                    elif query_choice == "2":
                        print("\n=== Сотрудники с количеством животных ===")
                        get_staff_with_animal_count(session)
                    elif query_choice == "3":
                        print("\n=== Загоны с количеством животных ===")
                        get_enclosures_with_animals(session)
                    elif query_choice == "4":
                        print("\n=== Детали ухода за животными ===")
                        get_care_records_with_details(session)
                    elif query_choice == "5":
                        print("\n=== Животные без записей об уходе ===")
                        get_animals_without_care_records(session)
                    elif query_choice == "6":
                        print("Возврат в главное меню...")
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")

            if choice == "2":
                while True:
                    display_json_operations_menu()
                    json_choice = input("Выберите операцию с JSON: ")

                    if json_choice == "1":
                        print("\n=== Экспорт данных из базы в JSON ===")
                        export_animals_to_json(session)
                    elif json_choice == "2":
                        print("\n=== Чтение данных из JSON ===")
                        read_animals_from_json()
                    elif json_choice == "3":
                        print("\n=== Обновление записи в JSON ===")
                        animal_id = 1
                        updates = {"age": 10, "name": "Big Lion"}
                        update_animal_in_json("animals.json", animal_id, updates)
                    elif json_choice == "4":
                        print("\n=== Добавление записи в JSON ===")
                        new_animal = {  # Пример данных нового животного
                            "name": "Elephant",
                            "species": "Loxodonta",
                            "type": "Mammals",
                            "age": 12,
                            "gender": "M",
                            "enclosure_id": 3
                        }
                        insert_animal_into_json("animals.json", new_animal)
                    elif json_choice == "5":
                        print("Возврат в главное меню...")
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")
            if choice == "3":
                while True:
                    display_database_operations_menu()
                    db_choice = input("Выберите операцию с базой данных: ")

                    if db_choice == "1":
                        print("\n=== Однотабличный запрос ===")
                        single_table_query(session, min_age=5)
                    elif db_choice == "2":
                        print("\n=== Многотабличный запрос ===")
                        multi_table_query(session)
                    elif db_choice == "3":
                        print("\n=== Добавление данных ===")
                        add_animal(session, "Panda", "Ailuropoda melanoleuca", "Mammals", 7, "F", 1)
                    elif db_choice == "4":
                        print("\n=== Изменение данных ===")
                        update_animal(session, 1, {"age": 10, "name": "Big Lion"})
                    elif db_choice == "5":
                        print("\n=== Удаление данных ===")
                        delete_animal(session, 2)
                    elif db_choice == "6":
                        print("\n=== Вызов хранимой процедуры ===")
                        call_stored_procedure(session)
                    elif db_choice == "7":
                        print("Возврат в главное меню...")
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")
            elif choice == "4":
                print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    main()
