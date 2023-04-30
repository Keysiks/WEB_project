from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from keyboards import Help_Menu_Keyboard, Week_Days, Day_Schedule
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import Database

from config import TOKEN

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

first_entrance = True


class BotStatesGroup(StatesGroup):
    monday = State()
    tuesday = State()
    wednesday = State()
    thursday = State()
    friday = State()
    saturday = State()
    homework = State()
    new_schedule = State()
    mark_and_lesson = State()
    lesson = State()


# сделать заполнение словаря уроков когда создается новое расписание

help_menu_keyboard = Help_Menu_Keyboard().return_keyboard()
week_days_keyboard = Week_Days().return_keyboard()
database = Database()

week_days = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота"}
schedule = Day_Schedule()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global first_entrance
    if first_entrance is True:
        database.drop_table()
        await message.reply("Привет! Чтобы узнать мои возможности вводи /help или /menu")
        await message.reply(
            "Сейчас тебе надо будет заполнить свое расписание. Сначала введи расписание на понедельник. "
            "Пиши каждый новый предемет через запятую")
        first_entrance = False
        await BotStatesGroup.monday.set()
    else:
        await bot.send_message(message.from_user.id, reply_markup=help_menu_keyboard, text="Вот мои функции:")


@dp.message_handler(commands=['help', "menu"])
async def process_help_command(message: types.Message):
    await bot.send_message(message.from_user.id, reply_markup=help_menu_keyboard, text="Вот мои функции:")


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('help_command'))
async def process_callback_help_commands(callback_query: types.CallbackQuery):
    code = int(callback_query.data[-1])
    if code == 0:
        await bot.send_message(callback_query.from_user.id, reply_markup=week_days_keyboard, text="Выбери день недели:")
    elif code == 1:
        pass
    elif code == 2:
        await bot.send_message(callback_query.from_user.id, text="Введи предмет, а затем оценку в этом же сообщении")
        await BotStatesGroup.mark_and_lesson.set()
    elif code == 3:
        await bot.send_message(callback_query.from_user.id, text="Введи предмет по которому хочешь узнать оценку")
        await BotStatesGroup.lesson.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('week_day'))
async def process_callback_week_days_commands(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    day_info = database.select_day(code)
    await bot.send_message(callback_query.from_user.id, text="Расписание:",
                           reply_markup=schedule.return_keyboard(day_info[1]))


@dp.message_handler(state=BotStatesGroup.monday)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[0] = message.text

    await message.reply("Теперь введи расписание на вторник")
    await BotStatesGroup.next()


@dp.message_handler(state=BotStatesGroup.tuesday)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[1] = message.text

    await message.reply("Теперь введи расписание на среду")
    await BotStatesGroup.next()


@dp.message_handler(state=BotStatesGroup.wednesday)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[2] = message.text

    await message.reply("Теперь введи расписание на четверг")
    await BotStatesGroup.next()


@dp.message_handler(state=BotStatesGroup.thursday)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[3] = message.text

    await message.reply("Теперь введи расписание на пятницу")
    await BotStatesGroup.next()


@dp.message_handler(state=BotStatesGroup.friday)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[4] = message.text

    await message.reply("Теперь введи расписание на субботу")
    await BotStatesGroup.next()


@dp.message_handler(state=BotStatesGroup.saturday)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[5] = message.text

    await message.reply("Ваше расписание успешно сохранено. Выйдите в меню командой /menu")
    await state.finish()
    database.enter_schedule(data)


@dp.message_handler(state=BotStatesGroup.mark_and_lesson)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data_mark:
        data_mark[0] = message.text

    await message.reply("Оценки успешно занесены")
    await state.finish()
    data = data_mark[0].replace(",", "")
    database.enter_mark(data.split(" ")[0], data.split(" ")[1])


@dp.message_handler(state=BotStatesGroup.lesson)
async def load_monday(message: types.Message, state: FSMContext):
    async with state.proxy() as data_lesson:
        data_lesson[0] = message.text

    data = data_lesson[0].strip()
    res = database.return_marks(data)
    await message.reply("Вот ваши оценки")
    await bot.send_message(message.from_user.id,
                           text=f"Список оценок: {' '.join(res[0][1:])}\nСреднее арифмитическое: {round(res[1], 2)}")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
