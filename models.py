import sqlite3
from sqlite3 import Error


class TodosSQLite:
    """sqlite3 database class that holds tasks"""

    def __init__(self, db_file):
        self.db_file = db_file

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(db_file)
        except Error:
            self.conn = None
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        with todos as cur:
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS todos (id integer PRIMARY KEY, title varchar(50), description text, done boolean)''')

    def add_todo(self, todo):
        with todos as cur:
            sql = '''INSERT INTO todos (title, description, done) VALUES(?,?,?)'''
            cur.execute(sql, todo)
        return cur.lastrowid

    def select_all(self, table):
        try:
            with todos as cur:
                sql = f'SELECT * FROM {table}'
                cur.execute(sql)
                rows = cur.fetchall()
                return rows
        except sqlite3.OperationalError as e:
            print(e)    
        

    def update(self, table, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )
        sql = f'UPDATE {table} SET {parameters} WHERE id = ?'
        try:
            with todos as cur:
                cur.execute(sql, values)
        except sqlite3.OperationalError as e:
            print(e)

    def delete_where(conn, table, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        sql = f'DELETE FROM {table} WHERE {q}'
        try:
            with todos as cur:
                cur.execute(sql, values)
        except sqlite3.OperationalError as e:
            print(e)


db_file = "./tasks_todo/todos.db"
todos = TodosSQLite(db_file)

if __name__ == '__main__':

    # todos.create_table()

    # todo = ('Szczepienie', 'Zadzwonić do punktu szczepień i zarejestrować się', False)
    # todos.add_todo(todo)

    # todos.update(todos, 3, done=True)

    print(todos.select_all(todos))
