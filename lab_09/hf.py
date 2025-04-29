import psycopg2
import redis
import json
from time import time
import matplotlib.pyplot as plt

REPS = 100


class StaffService:
    def __init__(self):
        print("Подключение к Redis...")
        self.__redis = redis.Redis(host='localhost', port=6379, db=0)

        try:
            info = self.__redis.info()
            print("Redis версия", info['redis_version'])
            response = self.__redis.ping()
            if response:
                print("Подключение к Redis выполнено успешно.")
            else:
                print("Не удалось подключиться к Redis.")
        except redis.exceptions.RedisError as e:
            print(f"Ошибка: {e}")

        print("Подключение к базе данных...")
        self.__conn = psycopg2.connect(dbname="zoo",
                                       user="xxx",
                                       password="xxx",
                                       host="localhost")
        print("Подключение к БД выполнено успешно.")
        self.__cursor = self.__conn.cursor()
        print("Готов к работе.")

    def __del__(self):
        print("Отключение от базы данных...")
        self.__cursor.close()
        self.__conn.close()
        print("Отключено.\nВыход...")

    def print_result(self, count):
        for i, el in enumerate(self.__cursor):
            if i == count:
                break
            print(el)

    def print_all_result(self):
        for i in self.__cursor:
            print(i)

    def select_staff(self):
        """Получение списка животных из базы данных"""
        sql_request = """
            SELECT name, position, age, hire_date FROM staff;
        """
        self.__cursor.execute(sql_request)

    def select_staff_redis(self):
        """Получение списка сотрудников через Redis"""
        cache = self.__redis.get('staff')
        if cache is not None:
            for i in json.loads(cache):
                print(i)
            return
        self.select_staff()
        res = self.__cursor.fetchall()
        for i in res:
            print(i)
        self.__redis.set('staff', json.dumps(res, default=str))

    def check_select_time(self):
        """Сравнение времени выполнения SELECT"""
        t1 = time()
        for _ in range(REPS):
            self.select_staff()
        t2 = time()

        res = self.__cursor.fetchall()
        cache = self.__redis.get('staff')
        if cache is None:
            self.__redis.set('staff', json.dumps(res, default=str))

        t3 = time()
        for _ in range(REPS):
            self.__redis.get('staff')
        t4 = time()

        plt.bar(["БД", "Redis"], [(t2 - t1) / REPS, (t4 - t3) / REPS])
        plt.title("Время SELECT в секундах")
        plt.savefig("1 сравнение времени выбора")

    def check_insert_time(self):
        """Сравнение времени выполнения INSERT"""
        staff = []
        t1 = time()
        for i in range(REPS):
            self.__cursor.execute(f"""
                INSERT INTO staff (name, position, age, hire_date)
                VALUES (%s, %s, %s, %s);
    """, ("Test User", "Keeper", 30, "2024-01-01"))
        t2 = time()
        self.__conn.commit()

        for i in range(REPS):
            name = f"'staff{i}'"
            self.__cursor.execute(f"SELECT * FROM staff WHERE name = {name}")
            staff.append(self.__cursor.fetchone())
            staff[i] = json.dumps(staff[i], default=str)

        t3 = time()
        for i in range(REPS):
            self.__redis.set(f'set{i}', staff[i])
        t4 = time()

        plt.bar(["БД", "Redis"], [(t2 - t1) / REPS, (t4 - t3) / REPS])
        plt.title("Время INSERT в секундах")
        plt.savefig("2 Сравнение времени вставки")

    def check_update_time(self):
        """Сравнение времени выполнения UPDATE"""
        staff = []
        t1 = time()
        for i in range(REPS):
            name = f"'staff{i}'"
            self.__cursor.execute(f"UPDATE staff SET age = age + 1 WHERE name = {name}")
        t2 = time()
        self.__conn.commit()

        for i in range(REPS):
            name = f"'staff{i}'"
            self.__cursor.execute(f"SELECT * FROM staff WHERE name = {name}")
            staff.append(self.__cursor.fetchone())
            staff[i] = json.dumps(staff[i], default=str)

        t3 = time()
        for i in range(REPS):
            self.__redis.set(f'staff{i}', staff[i])
        t4 = time()

        plt.bar(["БД", "Redis"], [(t2 - t1) / REPS, (t4 - t3) / REPS])
        plt.title("Время UPDATE в секундах")
        plt.savefig("3 Сравнение времени обновления")

    def check_delete_time(self):
        """Сравнение времени выполнения DELETE"""
        staff = []
        for i in range(REPS):
            name = f"'staff{i}'"
            self.__cursor.execute(f"SELECT * FROM staff WHERE name = {name}")
            staff.append(self.__cursor.fetchone())

        t1 = time()
        for i in range(REPS):
            name = f"'staff{i}'"
            self.__cursor.execute(f"DELETE FROM staff WHERE name = {name}")
        t2 = time()
        self.__conn.commit()

        t3 = time()
        for i in range(REPS):
            self.__redis.delete(f'staff{i}')
        t4 = time()

        plt.bar(["БД", "Redis"], [(t2 - t1) / REPS, (t4 - t3) / REPS])
        plt.title("Время DELETE в секундах")
        plt.savefig("4 Сравнение времени удаления")
