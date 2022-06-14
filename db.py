import sqlite3


class HouseDB:
    @staticmethod
    def query_res(sql):
        conn = sqlite3.connect('static/database/house.db')
        c = conn.cursor()

        cursor = c.execute(sql)

        return cursor
