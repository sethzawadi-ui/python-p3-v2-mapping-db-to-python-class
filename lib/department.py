# department.py
from __init__ import CONN, CURSOR

class Department:
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location
        if id:
            Department.all[id] = self

    # ---------------- Class methods for table management ---------------- #
    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()
        cls.all.clear()

    # ---------------- Instance methods ---------------- #
    def save(self):
        sql = """
        INSERT INTO departments (name, location)
        VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Department.all[self.id] = self

    def update(self):
        if not self.id:
            raise ValueError("Cannot update a department without an ID.")
        sql = """
        UPDATE departments
        SET name = ?, location = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()
        Department.all[self.id] = self

    def delete(self):
        if not self.id:
            return
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        Department.all.pop(self.id, None)
        self.id = None

    # ---------------- Class methods for CRUD ---------------- #
    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    @classmethod
    def instance_from_db(cls, row):
        if row is None:
            return None
        return cls(name=row[1], location=row[2], id=row[0])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row)
