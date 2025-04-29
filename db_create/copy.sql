COPY Enclosures (location, size, color, type)
FROM '/tmp/Enclosures.csv'
DELIMITER ','
CSV HEADER;

COPY Animals (name, species, type, age, gender, enclosure_id)
FROM '/tmp/Animals.csv'
DELIMITER ','
CSV HEADER;

COPY Staff (name, position, age, hire_date)
FROM '/tmp/Staff.csv'
DELIMITER ','
CSV HEADER;

COPY Care (animal_id, staff_id, care_date, description)
FROM '/tmp/Care.csv'
DELIMITER ','
CSV HEADER;