import sqlite3


class HouseDB:
    @staticmethod
    def query_res(sql):
        conn = sqlite3.connect('static/database/house.db')
        c = conn.cursor()

        cursor = c.execute(sql)

        return cursor

    @staticmethod
    def insert(sql):
        conn = sqlite3.connect('static/database/house.db')
        c = conn.cursor()

        try:
            c.execute(sql)
        except sqlite3.IntegrityError:
            return False

        conn.commit()
        return True
