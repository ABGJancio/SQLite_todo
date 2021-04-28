import sqlite3
from sqlite3 import Error


class TodosSQLite:
    """sqlite3 database class that holds tasks"""

    def __init__(self, db_file):
        self.db_file = db_file

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()
            return self.cur
        except Error:
            self.conn = None

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        with self as cur:
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS todos (id integer PRIMARY KEY, title varchar(50), description text, done boolean)''')

    def add_todo(self, todo):
        with self as cur:
            sql = '''INSERT INTO todos (title, description, done) VALUES(?,?,?)'''
            cur.execute(sql, todo)
        return cur.lastrowid

    def select_all(self):
        try:
            with self as cur:
                sql = f'SELECT * FROM todos'
                cur.execute(sql)
                row = cur.fetchall()
        except sqlite3.OperationalError as e:
            print(e)
        col = self.table_col()
        rows = []
        for i in range(len(row)):
            item = dict(zip(col, row[i]))
            rows.append(item)
        return rows
        
    def select_id(self, id):
        try:
            with self as cur:
                sql = f'SELECT * FROM todos WHERE id = {id}'
                cur.execute(sql)
                single_row = cur.fetchone()
        except sqlite3.OperationalError as e:
            print(e)    
        col = self.table_col()
        row = dict(zip(col, single_row))
        return row

    def update(self, table, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )
        sql = f'UPDATE {table} SET {parameters} WHERE id = ?'
        try:
            with self as cur:
                cur.execute(sql, values)
        except sqlite3.OperationalError as e:
            print(e)

    def delete_where(self, table, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        sql = f'DELETE FROM {table} WHERE {q}'
        try:
            with self as cur:
                cur.execute(sql, values)
        except sqlite3.OperationalError as e:
            print(e)

    def table_col(self):
        sql = 'PRAGMA table_info(todos)'
        try:
            with self as cur:
                cur.execute(sql)
                columns = [c[1] for c in cur.fetchall()]
                return columns
        except sqlite3.OperationalError as e:
            print(e)

db_file = "./tasks_todo/todos.db"
todos_db = TodosSQLite(db_file)

# if __name__ == '__main__':

#     # db_file = "./tasks_todo/todos.db"
#     # todos = TodosSQLite(db_file)
#     # todos.create_table()

#     # todo = ('Szczepienie', 'Zadzwonić do punktu szczepień i zarejestrować się', False)
#     # todos.add_todo(todo)

#     # todos.update("todos", 3, done=True)

#     print(todos.select_id(2))
