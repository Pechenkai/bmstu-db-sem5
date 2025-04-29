import psycopg2
from psycopg2.extras import RealDictCursor

from query import *

def connect_to_db():
    return psycopg2.connect(
        dbname="zoo",
        user="xxx",
        password="xxx",
        host="localhost",
        port=???
    )


def menu():
    connection = connect_to_db()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    functions = {
        1: scalar_query,
        2: join_query,
        3: cte_window_query,
        4: metadata_query,
        5: call_scalar_function,
        6: call_table_function,
        7: call_procedure,
        8: call_system_function,
        9: create_table,
        10: insert_data
    }

    while True:
        print("\n=== Меню операций с базой данных ===")
        print("1. Скалярный запрос")
        print("2. Запрос с несколькими соединениями (JOIN)")
        print("3. Запрос с ОТВ(CTE) и оконными функциями")
        print("4. Запрос к метаданным")
        print("5. Скалярная функцию")
        print("6. Табличная функцию")
        print("7. Хранимая процедура")
        print("8. Системная функция или процедура")
        print("9. Создать таблицу")
        print("10. Вставка данных")
        print("0. Выход")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input")
            connection.rollback()
            break

        if choice < 0 or choice > len(functions):
            print("Invalid input")
            connection.rollback()
            break

        if choice == 0:
            print("Exiting...")
            break
        elif choice in functions:
            try:
                functions[choice](cursor)
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                connection.rollback()
        else:
            print("Invalid option, please try again.")

    cursor.close()
    connection.close()


# Запуск программы
if __name__ == "__main__":
    menu()
