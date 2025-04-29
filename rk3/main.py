from peewee import *
from datetime import *
from requests import *

con = PostgresqlDatabase(
    database='rk3',
    user='xxx',
    password='xxx',
    host='localhost',
    port="???"
)


class BaseModel(Model):
    class Meta:
        database = con


class Satellite(BaseModel):
    id = IntegerField(column_name='id')
    name = CharField(column_name='name')
    date = DateField(column_name='date')
    country = CharField(column_name='country')

    class Meta:
        table_name = 'satellite'


class Flight(BaseModel):
    id = IntegerField(column_name='id')
    sat_id = ForeignKeyField(Satellite, backref='sat_id')
    date = DateField(column_name='date')
    time = TimeField(column_name='time')
    day = CharField(column_name='day')
    type = IntegerField(column_name='type')

    class Meta:
        table_name = 'flight'


def sql():
    global con

    cur = con.cursor()

    cur.execute(Querry1)
    print("Первый запрос:\n")
    rows = cur.fetchall()
    for row in rows:
        print(*row)

    print()

    cur.execute(Querry2)
    print("Второй запрос:\n")
    rows = cur.fetchall()
    for row in rows:
        print(*row)

    print()

    cur.execute(Querry3)
    print("\nТретий запрос:\n")
    rows = cur.fetchall()
    for row in rows:
        print(*row)

    print("Все запросы выполнены.")
    cur.close()


def orm():
    global con

    cur = con.cursor()

    print("Найти самый древний спутник России:")
    query = Satellite.select().where(Satellite.country == 'Россия').order_by(Satellite.date).limit(1)
    for q in query.dicts().execute():
        print(q)

    print("Найти спутники, которые не возвращались в течение этого календарного года:")
    query = Satellite.select(Satellite.id, Satellite.name).join(Flight, JOIN.LEFT_OUTER, on=(
            (Satellite.id == Flight.sat_id) &
            (Flight.type == 0) &
            (Flight.date.year == datetime.now().year)
    )).where(Flight.id.is_null())
    for q in query.dicts().execute():
        print(q)

    print("Найти все аппараты, вернувшиеся на землю не позднее 10 дней с 2024-01-01:")
    query = (Satellite
             .select(Satellite.id, Satellite.name)
             .join(Flight, on=(Satellite.id == Flight.sat_id))
             .where(
        (Flight.type == 0) &
        (Flight.date.between('2024-01-01', '2024-01-11')))
             .group_by(Satellite.id))
    for q in query.dicts().execute():
        print(q)

    cur.close()


def main():
    sql()
    orm()

    con.close()


if __name__ == "__main__":
    main()
