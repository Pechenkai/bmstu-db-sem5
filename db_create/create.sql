CREATE TABLE if not exists Enclosures (
    id SERIAL PRIMARY KEY,
    location TEXT,
    size DECIMAL(5,2),
    color TEXT,
    type TEXT
);

CREATE TABLE if not exists Animals (
    id SERIAL PRIMARY KEY,
    name TEXT,
    species TEXT,
    type TEXT,
    age INT,
    gender CHAR(1),
    enclosure_id INT
);

CREATE TABLE if not exists Staff (
    id SERIAL PRIMARY KEY,
    name TEXT,
    position TEXT,
    age INT,
    hire_date DATE
);

CREATE TABLE if not exists Care (
    id SERIAL PRIMARY KEY,
    animal_id INT,
    staff_id INT,
    care_date DATE,
    description TEXT
);