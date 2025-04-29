from sqlalchemy.orm import Session
from tables import Animal, Enclosure

from sqlalchemy.sql import text


# Запрос для получения всех животных старше определенного возраста.
def single_table_query(session: Session, min_age: int):
    """
    SELECT * FROM Animals WHERE age > :min_age
    """
    results = session.query(Animal).filter(Animal.age > min_age).all()
    for animal in results:
        print(f"ID: {animal.id}, Name: {animal.name}, Age: {animal.age}, Species: {animal.species}")


# Запрос для получения списка животных с именами загонов, в которых они находятся.
def multi_table_query(session: Session):
    """
    SELECT Animals.name, Animals.species, Enclosures.location
    FROM Animals
    JOIN Enclosures ON Animals.enclosure_id = Enclosures.id
    """
    results = session.query(Animal.name, Animal.species, Enclosure.location) \
        .join(Enclosure, Animal.enclosure_id == Enclosure.id).all()
    for name, species, location in results:
        print(f"Animal: {name}, Species: {species}, Enclosure Location: {location}")


def add_animal(session: Session, name: str, species: str, animal_type: str, age: int, gender: str, enclosure_id: int):
    """
    INSERT INTO Animals (name, species, type, age, gender, enclosure_id)
    VALUES (:name, :species, :animal_type, :age, :gender, :enclosure_id)
    """
    new_animal = Animal(
        name=name,
        species=species,
        type=animal_type,
        age=age,
        gender=gender,
        enclosure_id=enclosure_id
    )
    session.add(new_animal)
    session.commit()
    print(f"Добавлено новое животное: {name}")


def update_animal(session: Session, animal_id: int, updates: dict):
    """
    UPDATE Animals SET column = value WHERE id = :animal_id
    """
    animal = session.query(Animal).filter(Animal.id == animal_id).first()
    if animal:
        for key, value in updates.items():
            setattr(animal, key, value)
        session.commit()
        print(f"Животное с ID {animal_id} обновлено.")
    else:
        print(f"Животное с ID {animal_id} не найдено.")


def delete_animal(session: Session, animal_id: int):
    """
    DELETE FROM Animals WHERE id = :animal_id
    """
    animal = session.query(Animal).filter(Animal.id == animal_id).first()
    if animal:
        session.delete(animal)
        session.commit()
        print(f"Животное с ID {animal_id} удалено.")
    else:
        print(f"Животное с ID {animal_id} не найдено.")


def call_stored_procedure(session: Session):
    """
    CALL count_animals_per_enclosure()
    """
    sql = text("SELECT * FROM count_animals_per_enclosure()")
    result = session.execute(sql)
    for row in result:
        print(f"Enclosure ID: {row.enclosure_id}, Animal Count: {row.animal_count}")
