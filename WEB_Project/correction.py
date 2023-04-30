import sqlite3
import json

connection = sqlite3.connect("schedule.db")
cursor = connection.cursor()

lesson = "физика"
cursor.execute(f"""UPDATE lessons SET marks='{json.dumps([0, 5, 4, 5])}' WHERE lesson_name={(f'"{lesson.lower()}"')}""")


print(cursor.execute(f"""SELECT * FROM lessons WHERE lesson_name={(f'"{lesson.lower()}"')}""").fetchone()[2])
# образец запроса

res = json.loads(cursor.execute(f"""SELECT marks FROM lessons WHERE lesson_name={(f'"{lesson.lower()}"')}""").fetchone()[0])
print([res, sum([int(i) for i in res])/(len(res) - 1)])