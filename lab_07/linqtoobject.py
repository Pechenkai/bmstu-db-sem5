from sqlalchemy.orm import Session
from tables import Animal, Enclosure, Staff, Care
from sqlalchemy.sql import func


# Находит животных старше указанного возраста, упорядочивая их по возрасту в обратном порядке.
def get_animals_by_age(session: Session, min_age: int):
    """
    SELECT name, species, age FROM Animals WHERE age >= :min_age ORDER BY age DESC LIMIT 5
    """
    data = session.query(Animal.name, Animal.species, Animal.age) \
        .filter(Animal.age >= min_age) \
        .order_by(Animal.age.desc()) \
        .limit(5).all()
    for row in data:
        print(f"Name: {row.name}, Species: {row.species}, Age: {row.age}")


# Выводит сотрудников и количество животных, за которыми они ухаживают, при этом учитываются только те, у кого больше
# одного животного.
def get_staff_with_animal_count(session: Session):
    """
    SELECT Staff.name, COUNT(Care.animal_id) as animal_count
    FROM Staff
    JOIN Care ON Staff.id = Care.staff_id
    GROUP BY Staff.id, Staff.name
    HAVING COUNT(Care.animal_id) > 1
    ORDER BY animal_count DESC
    """
    data = session.query(Staff.name, func.count(Care.animal_id).label('animal_count')) \
        .join(Care, Staff.id == Care.staff_id) \
        .group_by(Staff.id, Staff.name) \
        .having(func.count(Care.animal_id) > 1) \
        .order_by(func.count(Care.animal_id).desc()).all()
    for row in data:
        print(f"Staff Name: {row.name}, Animal Count: {row.animal_count}")


# Подсчитывает количество животных в каждом загоне, включая загоны без животных.
def get_enclosures_with_animals(session: Session):
    """
    SELECT Enclosures.location, Enclosures.type, COUNT(Animals.id) as animal_count
    FROM Enclosures
    LEFT JOIN Animals ON Enclosures.id = Animals.enclosure_id
    GROUP BY Enclosures.id, Enclosures.location, Enclosures.type
    ORDER BY animal_count DESC
    """
    data = session.query(Enclosure.location, Enclosure.type, func.count(Animal.id).label('animal_count')) \
        .outerjoin(Animal, Enclosure.id == Animal.enclosure_id) \
        .group_by(Enclosure.id, Enclosure.location, Enclosure.type) \
        .order_by(func.count(Animal.id).desc()).all()
    for row in data:
        print(f"Location: {row.location}, Type: {row.type}, Animal Count: {row.animal_count}")


# Выводит подробности об уходе за животными, включая дату, животное, сотрудника и описание.
def get_care_records_with_details(session: Session):
    """
    SELECT Care.care_date, Animals.name, Staff.name, Care.description
    FROM Care
    JOIN Animals ON Care.animal_id = Animals.id
    JOIN Staff ON Care.staff_id = Staff.id
    ORDER BY Care.care_date DESC
    """
    data = session.query(Care.care_date, Animal.name.label('animal_name'), Staff.name.label('staff_name'),
                         Care.description) \
        .join(Animal, Care.animal_id == Animal.id) \
        .join(Staff, Care.staff_id == Staff.id) \
        .order_by(Care.care_date.desc()).all()
    for row in data:
        print(
            f"Date: {row.care_date}, Animal: {row.animal_name}, Staff: {row.staff_name}, Description: {row.description}")


# Находит всех животных, у которых нет записей об уходе.
def get_animals_without_care_records(session: Session):
    """
    SELECT Animals.name, Animals.species
    FROM Animals
    LEFT JOIN Care ON Animals.id = Care.animal_id
    WHERE Care.id IS NULL
    """
    data = session.query(Animal.name, Animal.species) \
        .outerjoin(Care, Animal.id == Care.animal_id) \
        .filter(Care.id == None).all()
    for row in data:
        print(f"Animal: {row.name}, Species: {row.species}")
