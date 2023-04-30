from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import Database

database = Database()


class Help_Menu_Keyboard:
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup()
        self.help_menu_commands = ["Узнать расписание", "Занести дз", "Занести оценку", "Узнать оценки"]
        for i in range(len(self.help_menu_commands)):
            self.keyboard.add(InlineKeyboardButton(self.help_menu_commands[i], callback_data=f'help_command{i}'))

    def return_keyboard(self):
        return self.keyboard


class Week_Days:
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup()
        self.week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        for i in range(len(self.week_days)):
            self.keyboard.add(
                InlineKeyboardButton(self.week_days[i], callback_data=f"week_day{i}"))

    def return_keyboard(self):
        return self.keyboard


class Day_Schedule:
    def __init__(self):
        pass
    
    def return_keyboard(self, lessons):
        lessons = [i.strip() for i in lessons]
        keyboard = InlineKeyboardMarkup()
        for i in range(len(lessons)):
            keyboard.add(InlineKeyboardButton(lessons[i].capitalize(),
                                              callback_data=f"lesson{lessons[i]}"))
        return keyboard


class Marks:
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup()
        for i in range(1, 6):
            self.keyboard.add(InlineKeyboardButton(str(i), callback_data=f"mark{i}"))

    def return_keyboard(self):
        return self.keyboard


class Lessons:
    def __init__(self):
        self.lessons = database.return_lessons()
        self.keyboard = InlineKeyboardMarkup()
        for i in range(len(self.lessons)):
            self.keyboard.add(InlineKeyboardButton(self.lessons[i], callback_data=f"lessonmark{self.lessons[i]}"))

    def return_keyboard(self):
        return self.keyboard