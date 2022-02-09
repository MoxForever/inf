import sqlite3

db = sqlite3.connect(input("ПУть к базе: ").strip())
db.row_factory = sqlite3.Row
cursor = db.cursor()
cursor.execute("SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")
a = cursor.fetchall()
tables = [i[0] for i in a]

now_table = None
now_table_rows = None
while True:
    if now_table is None:
        tables_str = str(tables)[1:-1].replace("'", '')
        table = input(f"Выберете таблицу для работы ({tables_str}): ").strip()
        if table in tables:
            now_table = table
        else:
            print("Такой таблицы не существует")
    else:
        cursor.execute(f"SELECT * FROM {now_table} LIMIT 1")
        if now_table_rows is None:
            now_table_rows = list(dict(cursor.fetchall()[0]).keys())

        now_table_rows_str = ""
        for i in now_table_rows:
            now_table_rows_str += i + " | "
        now_table_rows_str = now_table_rows_str[:-3]

        print(f"Таблица: {now_table}\n{now_table_rows_str}")
        cmd = input("Действие (insert, select, delete): ")
        if cmd == "select":
            cursor.execute(f"SELECT * FROM {now_table}")
            max_row_w = [0] * len(now_table_rows)
            data = [dict(i) for i in cursor.fetchall()]
            q = 0
            for i in now_table_rows:
                max_row_w[q] = max(max_row_w[q], len(i))
                q += 1
            for i in data:
                q = 0
                for j in i.keys():
                    max_row_w[q] = max(max_row_w[q], len(str(i[j])))
                    q += 1
            for i in range(len(data)):
                q = 0
                for j in data[i].keys():
                    data[i][j] = str(data[i][j]) + " " * (max_row_w[q] - len(str(data[i][j])))
                    q += 1

            q = 0
            for i in now_table_rows:
                print(i+" " * (max_row_w[q] - len(i)), end=" | ")
                q += 1
            print()
            for i in data:
                for j in i.values():
                    print(j, end=" | ")
                print()
            print()

        elif cmd == "insert":
            print(f"Таблица: {now_table}\n{now_table_rows_str}")
            args = input("Введите значения столбцов через запятую (строки брать в одинарные кавычки): ")
            try:
                cursor.execute(f"INSERT INTO {now_table} VALUES ({args})")
                db.commit()
            except Exception as ex:
                print(f"Возникла ошибка: {ex}")
            else:
                print("Успешно")
            print()

        elif cmd == "delete":
            args = input("Введите условие, по которому удалять записи (пример id = 727): ")
            try:
                cursor.execute(f"DELETE FROM {now_table} WHERE {args}")
                db.commit()
            except Exception as ex:
                print(f"Возникла ошибка: {ex}")
            else:
                print(f"Строк удалено: {cursor.rowcount}")
            print()

