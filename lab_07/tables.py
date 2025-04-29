from sqlalchemy import (
    Column, Integer, ForeignKey, Text, Date, CheckConstraint, DECIMAL, CHAR
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Enclosure(Base):
    __tablename__ = 'enclosures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(Text, nullable=False)
    size = Column(DECIMAL(5, 2), nullable=False)
    color = Column(Text, nullable=True)
    type = Column(Text, nullable=False)

    animals = relationship("Animal", back_populates="enclosure", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("size > 0", name="size_val"),
    )


class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    species = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(CHAR(1), nullable=False)
    enclosure_id = Column(Integer, ForeignKey('enclosures.id', ondelete="CASCADE"), nullable=False)

    enclosure = relationship("Enclosure", back_populates="animals")
    care = relationship("Care", back_populates="animal", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("age > 0", name="age_val"),
        CheckConstraint("gender IN ('M', 'F')", name="gen_val"),
    )


class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    position = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    hire_date = Column(Date, nullable=False)

    care = relationship("Care", back_populates="staff", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("age > 0", name="age_val_s"),
        CheckConstraint("hire_date > '1970-01-01' AND hire_date <= current_date", name="hire_val"),
    )


class Care(Base):
    __tablename__ = 'care'

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animals.id', ondelete="CASCADE"), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.id', ondelete="CASCADE"), nullable=False)
    care_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)

    animal = relationship("Animal", back_populates="care")
    staff = relationship("Staff", back_populates="care")

    __table_args__ = (
        CheckConstraint("care_date > '1970-01-01' AND care_date <= current_date", name="cdate_val"),
    )


