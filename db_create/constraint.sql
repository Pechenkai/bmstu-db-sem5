ALTER TABLE animals
    ADD CONSTRAINT fk_ae FOREIGN KEY (enclosure_id) REFERENCES enclosures(id);
ALTER TABLE animals
    ADD CONSTRAINT age_val CHECK (age > 0);
ALTER TABLE animals
    ADD CONSTRAINT gen_val CHECK (gender IN ('M', 'F'));  
    
ALTER TABLE enclosures 
    ADD CONSTRAINT size_val CHECK (size > 0);
    
ALTER TABLE staff 
    ADD CONSTRAINT age_val_s CHECK (age > 0);
ALTER TABLE staff 
    ADD CONSTRAINT hire_val CHECK (hire_date > '1970-01-01'::date AND hire_date <= current_date);
    
ALTER TABLE care 
    ADD CONSTRAINT fk_ca FOREIGN KEY (animal_id) REFERENCES animals(id) on delete CASCADE;
ALTER TABLE care 
    ADD CONSTRAINT fk_cs FOREIGN KEY (staff_id) REFERENCES staff(id) on delete CASCADE;
ALTER TABLE care 
    ADD CONSTRAINT cdate_val CHECK (care_date > '1970-01-01'::date AND care_date <= current_date);
    
CREATE OR REPLACE FUNCTION check_animal_enclosure_type()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT type FROM enclosures WHERE id = NEW.enclosure_id) <> NEW.type THEN
        RAISE EXCEPTION 'Тип животного (%) не соответствует типу загона (%)', NEW.type, (SELECT type FROM enclosures WHERE id = NEW.enclosure_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_animal_type
BEFORE INSERT OR UPDATE ON animals
FOR EACH ROW
EXECUTE FUNCTION check_animal_enclosure_type();