import sqlite3
import json


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("schedule.db")
        self.cursor = self.connection.cursor()

    def new_table(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS week_days(
                                    day_id INT PRIMARY KEY,
                                    lessons JSON);""")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS lessons(
                                    lesson_name TEXT PRIMARY KEY,
                                    homework TEXT,
                                    marks JSON);""")

        self.connection.commit()

    def select_day(self, day_id):
        try:
            print(day_id)
            day_info = self.cursor.execute(f"""SELECT * FROM week_days WHERE day_id={day_id}""").fetchall()
            return [day_info[0][0], json.loads(day_info[0][1])]
        except TypeError:
            print("wrong day")

    def enter_schedule(self, schedule):
        self.lst = []
        for i in range(6):
            day_schedule = schedule[i].split(",")
            day_schedule = [k.strip() for k in day_schedule]
            for j in range(len(day_schedule)):
                if day_schedule[j].lower() not in self.lst:
                    print(day_schedule[j])
                    self.cursor.execute(f"""INSERT INTO lessons VALUES(?, ?, ?);""", (day_schedule[j].lower(), "", json.dumps([0])))
                    self.lst.append(day_schedule[j].lower())
        for i in range(6):
            self.cursor.execute(f"""INSERT INTO week_days VALUES(?, ?);""", (i, json.dumps(schedule[i].lower().split(","))))
        self.connection.commit()

    def enter_mark(self, lesson, mark):
        lst = json.loads(self.cursor.execute(f"""SELECT * FROM lessons WHERE lesson_name={(f'"{lesson.lower()}"')}""").fetchone()[2])
        lst.append(int(mark))
        lst = json.dumps(lst)
        self.cursor.execute(f"""UPDATE lessons SET marks = '{lst}' WHERE lesson_name={(f'"{lesson.lower()}"')}""")
        self.connection.commit()

    def drop_table(self):
        self.cursor.execute(f"""DROP TABLE IF EXISTS week_days""")
        self.cursor.execute(f"""DROP TABLE IF EXISTS lessons""")
        self.new_table()

    def return_marks(self, lesson):
        res = json.loads(self.cursor.execute(f"""SELECT marks FROM lessons WHERE lesson_name={(f'"{lesson.lower()}"')}""").fetchone()[0])
        return [res, sum([int(i) for i in res])/(len(res) - 1)]

    def return_lessons(self):
        return self.lst

    def enter_homework(self, lesson, homework):
        self.cursor.execute(f"""UPDATE lessons SET homework='{homework}' WHERE lesson_name={(f'"{lesson.lower()}"')}""")
        self.connection.commit()

    def return_homework(self, lesson):
        return self.cursor.execute(f"""SELECT homework FROM lessons WHERE lesson_name={(f'"{lesson.lower()}"')}""").fetchone()