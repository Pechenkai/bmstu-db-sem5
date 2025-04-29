import json
import os
from datetime import datetime
from time import sleep
from faker import Faker

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

enclosure_colors = ["Green", "Blue", "Yellow", "Red", "Brown", "Gray", "White"]


def generate_enclosures(num_enclosures):
    enclosures = []
    for i in range(2):
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


def generate_file():
    table_name = "enclosures"
    data = []
    for i in range(2):
        enclosure_type = random.choice(list(animals_by_type.keys()))
        enclosure = {
            "Location": f"Zone_{random.randint(1, 20)}",
            "Size": round(random.uniform(100, 1000), 2),
            "Color": random.choice(enclosure_colors),
            "Type": enclosure_type
        }
        data.append(enclosure)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"zoo_{table_name}_{timestamp}.json"

    os.makedirs("output", exist_ok=True)
    with open(os.path.join("./output/", filename), "w") as file:
        json.dump(data, file, indent=4)


while True:
    generate_file()
    print("File generated!")
    sleep(300)
