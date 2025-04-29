from faker import Faker
import csv
import random

animals_by_type = {
    "BigCat": ["Lion", "Tiger", "Leopard", "Pantera"],
    "Forrest": ["Grizzly", "Panda", "Coala"],
    "SmallBird": ["Chicken", "Parrot", "Pigeon", "Mocking bird", "Peacock", "Canary"],
    "MiddleBird": ["Pelican", "Goose", "Flamingo", "Ostrich", "Swan"],
    "BirdPredator": ["Penguin", "Falcon", "Owl", "Hawk", "Vulture"],
    "SeaAnimal": ["Shark", "Seal", "Walrus", "Sea lion", "Dolphin"],
    "Fish": ["Salmon", "Bass", "Guitarfish", "Trout"],
    "Primate": ["Gorilla", "Chimpanzee", "Orangutan"]
}

staff_positions = ["Keeper", "Veterinarian", "Cleaner", "Zoologist", "Breeding Specialist", "Animal Trainer",
                   "Nutritionist"]

enclosure_colors = ["Green", "Blue", "Yellow", "Red", "Brown", "Gray", "White"]


def generate_enclosures(num_enclosures):
    enclosures = []
    for i in range(num_enclosures):
        enclosure_type = random.choice(list(animals_by_type.keys()))
        enclosure = {
            "ID": i + 1,
            "Location": f"Zone_{random.randint(1, 20)}",
            "Size": round(random.uniform(100, 1000), 2),
            "Color": random.choice(enclosure_colors),
            "Type": enclosure_type
        }
        enclosures.append(enclosure)
    return enclosures


def generate_animals(num_animals, enclosures):
    animals = []
    fake = Faker()

    # Группируем вольеры по типу в виде списков
    enclosure_dict = {}
    for enclosure in enclosures:
        if enclosure["Type"] not in enclosure_dict:
            enclosure_dict[enclosure["Type"]] = []
        enclosure_dict[enclosure["Type"]].append(enclosure)

    for i in range(num_animals):
        enclosure_type = random.choice(list(animals_by_type.keys()))

        species = random.choice(animals_by_type[enclosure_type])

        enclosure = random.choice(enclosure_dict[enclosure_type])

        animal = {
            "ID": i + 1,
            "Name": fake.first_name(),
            "Species": species,
            "Type": enclosure_type,
            "Age": random.randint(1, 20),
            "Gender": random.choice(["M", "F"]),
            "EnclosureID": enclosure["ID"]
        }
        animals.append(animal)

    return animals


def generate_staff(num_staff):
    fake = Faker()
    staff = []
    for i in range(num_staff):
        staff.append({
            "ID": i + 1,
            "Name": f"{fake.name()}",
            "Position": random.choice(staff_positions),
            "Age": random.randint(18, 60),
            "HireDate": f"20{random.randint(10, 23)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        })
    return staff


def generate_care_data(animals, staff, enclosures, num_records):
    care_records = []
    for i in range(num_records):
        animal = random.choice(animals)
        staff_member = random.choice(staff)
        care_records.append({
            "ID": i + 1,
            "AnimalID": animal["ID"],
            "StaffID": staff_member["ID"],
            "CareTime": f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00",
            "Notes": f"Care record {i + 1}"
        })
    return care_records


def write_csv(filename, fieldnames, data):
    if "ID" in fieldnames:
        fieldnames = [field for field in fieldnames if field != "ID"]

    for row in data:
        if "ID" in row:
            del row["ID"]

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    num_enclosures = 1000
    num_animals = 3000
    num_staff = 1500
    num_care_records = 3000

    enclosures = generate_enclosures(num_enclosures)

    animals = generate_animals(num_animals, enclosures)

    staff = generate_staff(num_staff)

    care_data = generate_care_data(animals, staff, enclosures, num_care_records)

    write_csv("/tmp/Enclosures.csv", ["ID", "Location", "Size", "Color", "Type"], enclosures)
    write_csv("/tmp/Animals.csv", ["ID", "Name", "Species", "Type", "Age", "Gender", "EnclosureID"], animals)
    write_csv("/tmp/Staff.csv", ["ID", "Name", "Position", "Age","HireDate"], staff)
    write_csv("/tmp/Care.csv", ["ID", "AnimalID", "StaffID", "CareTime", "Notes"], care_data)


if __name__ == "__main__":
    main()