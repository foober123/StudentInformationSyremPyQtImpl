from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import random
from faker import Faker
from datetime import datetime
from collections import defaultdict

fake = Faker()

PROGRAMS = ["BSCS", "BSIT", "BSCA", "BSCE", "BSA"]
GENDERS = ["Male", "Female", "Other"]

def generate_student_id(year, index):
    return f"{year}-{index:04d}"

def seed_students(count=10000):
    db = QSqlDatabase.database()
    db.transaction()

    current_year = datetime.now().year
    values = []

    year_counters = defaultdict(int)

    for _ in range(count):
        year_prefix = random.randint(current_year - 5, current_year)

        year_counters[year_prefix] += 1
        sequence = year_counters[year_prefix]

        student_id = generate_student_id(year_prefix, sequence)

        firstname = fake.first_name().replace("'", "''")
        lastname = fake.last_name().replace("'", "''")
        course = random.choice(PROGRAMS)
        year = random.randint(1, 5)
        gender = random.choice(GENDERS)

        values.append(
            f"('{student_id}', '{firstname}', '{lastname}', '{course}', {year}, '{gender}')"
        )

    sql = f"""
    INSERT INTO student (id, firstname, lastname, course, year, gender)
    VALUES
    {",\n".join(values)}
    """

    query = QSqlQuery()

    if not query.exec(sql):
        print("Insert Error:", query.lastError().text())
        db.rollback()
    else:
        db.commit()
        print(f"Inserted {count} students successfully")
