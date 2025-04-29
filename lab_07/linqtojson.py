import json
from sqlalchemy.orm import Session
from tables import Animal


def export_animals_to_json(session: Session, filename: str = "animals.json"):
    """
    Экспорт данных из таблицы Animals в JSON файл.
    """
    data = session.query(Animal).all()
    animals = [
        {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "type": animal.type,
            "age": animal.age,
            "gender": animal.gender,
            "enclosure_id": animal.enclosure_id
        }
        for animal in data
    ]

    with open(filename, "w") as file:
        json.dump(animals, file, indent=4)

    print(f"Данные экспортированы в файл {filename}")


def read_animals_from_json(filename: str = "animals.json"):
    """
    Чтение данных из JSON файла.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for animal in data:
                print(animal)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Сначала выполните экспорт данных.")


def update_animal_in_json(filename: str, animal_id: int, updates: dict):
    """
    Обновление записи в JSON файле.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)

        updated = False
        for animal in data:
            if animal["id"] == animal_id:
                animal.update(updates)
                updated = True
                break

        if updated:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Животное с ID {animal_id} обновлено.")
        else:
            print(f"Животное с ID {animal_id} не найдено.")

    except FileNotFoundError:
        print(f"Файл {filename} не найден. Сначала выполните экспорт данных.")


def insert_animal_into_json(filename: str, new_animal: dict):
    """
    Добавление новой записи в JSON файл.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)

        # Генерируем новый ID
        max_id = max([animal["id"] for animal in data], default=0)
        new_animal["id"] = max_id + 1

        data.append(new_animal)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Новое животное добавлено с ID {new_animal['id']}.")
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Сначала выполните экспорт данных.")