from hf import StaffService

def menu():
    print("Меню:")
    print("In-Memory DataBase на примере Redis")
    print("1 - Получить список сотрудников из БД")
    print("2 - Приложение выполняет запрос на стороне БД")
    print("3 - Приложение выполняет запрос через Redis")
    print("4 - Сравнительный анализ select")
    print("5 - Сравнительный анализ insert")
    print("6 - Сравнительный анализ update")
    print("7 - Сравнительный анализ delete")
    print("0 - Выход")

db = StaffService()
top = 10

while True:
    menu()
    action = int(input("Введите номер действия: "))
    if action == 1:
        db.select_staff()
        db.print_result(top)
    elif action == 2:
        db.select_staff()
        db.print_all_result()
    elif action == 3:
        db.select_staff_redis()
    elif action == 4:
        db.check_select_time()
    elif action == 5:
        db.check_insert_time()
    elif action == 6:
        db.check_update_time()
    elif action == 7:
        db.check_delete_time()
    else:
        break