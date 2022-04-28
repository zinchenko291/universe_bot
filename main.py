# ссылка на бота https://t.me/Bot_Encyclopedia_Bot

import logging
import asyncio
import os

from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

class StateMachine(StatesGroup):
    playOrNot = State()
    firstMove = State()
    A1 = State()
    A2 = State()
    A3 = State()
    B1 = State()
    B2 = State()
    B3 = State()
    A4 = State()
    B4 = State()

chessPath = os.getenv('CHESS_PATH')

@dp.message_handler(commands = ['start', 'help'], state='*')
async def main_function(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add('Конечно сыграю', 'Извини, но нет')
    await message.answer(f'Здравствуйте! Я - бот! Приветствую, {message.from_user.first_name}. Вы готовы сразиться со мной и помериться силой в знаниях и умениях. Предлагаю сыграть в игру. Сыграем?', reply_markup = markup)
    logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Начал играть')
    await StateMachine.playOrNot.set()

@dp.message_handler(state=StateMachine.playOrNot)
async def checking_the_main_question(message: types.Message, state: FSMContext):
    # проверка гл вопроса
    if message.text == 'Конечно сыграю':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Согласился играть')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True, row_width = 1).add('Я буду ходить первым', 'Можешь ходить первым')
        await message.answer_photo(types.InputFile(chessPath + '1.png'), 'Круто, вот как будет выглядеть доска, на которой Вы будете играть против меня.\nВыбирай кто будет ходить первый', reply_markup = markup)
        await StateMachine.firstMove.set()
    else:
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Отказался играть')
        await message.answer('Жаль, как захочешь сыграть, напиши мне /start и мы сыграем')
        await state.reset_state(with_data=False)

@dp.message_handler(state=StateMachine.firstMove)
async def the_first_move(message: types.Message):
    # первый ход
    if message.text == 'Я буду ходить первым':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Будет ходить первым')
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item_button = types.InlineKeyboardButton(text = 'Ходить на клетку E3')
        markup.add(item_button)
        await message.answer_photo(types.InputFile(chessPath + '1.png'), 'Хорошо, ты играешь за белую команду, первый ход делается пешкой которая находится на E2, выбирай клетку на которую хочешь ходить', reply_markup = markup)
        await StateMachine.B1.set()
    else:
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Будет ходить вторым')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Ходить на клетку E3')
        await message.answer_photo(types.InputFile(chessPath + '5.png'), 'Спасибо, что уступил мне. Я сходил пешкой которая стояла на F7, а теперь стоит на F5.')
        await message.answer('Теперь твой ход. Куда хочешь ходить пешкой которая стоит на E2, выбери из списка ниже:', reply_markup = markup)
        await StateMachine.A1.set()

@dp.message_handler(state=StateMachine.A1)
async def A1(message: types.Message):
    # первый ход противника
    if message.text == 'Ходить на клетку E3':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Задача с печеньем')
        markup = types.ReplyKeyboardRemove()
        await message.answer('Постой, перед тем как сделать ход выполни задание: Печенье упаковали в пачки по 250 г. Пачки сложили в ящик в 4 слоя. Каждый слой имеет 5 рядов по 6 пачек в каждом. Выдержит ли ящик, если максимальная масса, на которую он рассчитан, равна 32 кг? Напишите да или нет.', reply_markup = markup)
        await StateMachine.A2.set()
    else:
        await message.answer('😔 На эту позицию нельзя ходить.')

@dp.message_handler(state=StateMachine.A2)
async def A2(message: types.Message):
    # сходить 2 раз
    if message.text.lower() == 'да':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True).add('Сходить на H5')
        await message.answer_photo(types.InputFile(chessPath + '7.png'), 'Молодец, правильно решил задание, я хожу пешкой которая стояла на G7, а теперь она стоит на G5')
        await message.answer('А ты куда пойдешь королевой, которая стоит на D1', reply_markup = markup)
        await StateMachine.A3.set()
    else:
        await message.answer('Ты ошибся. Попробуй ещё раз.')

@dp.message_handler(state=StateMachine.A3)
async def A3(message: types.Message):
    # последних ход
    if message.text == 'Сходить на H5':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Задача графиком')
        markup = types.ReplyKeyboardRemove()
        await message.answer_photo(types.InputFile('exercise.jpg'), 'Постой, перед тем как сделать ход выполни задание. Ответ запиши цифрами, без пробелов.', reply_markup=markup)
        await StateMachine.A4.set()
    else:
        await message.answer('😔 На эту позицию нельзя ходить.')

@dp.message_handler(state=StateMachine.A4)
async def A4(message: types.Message, state: FSMContext):
    # финал
    if message.text == '2314':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Закончил играть')
        markup = types.ReplyKeyboardRemove()
        await message.answer_photo(types.InputFile(chessPath + '8.png'), 'ПОЗДРАВЛЯЮ!!! Вы выиграли!!! Вы сделали шах и мат мне. Чтобы начать заново напишите /start', reply_markup=markup)
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ты ошибся. Попробуй ещё раз.')

        
@dp.message_handler(state=StateMachine.B1)
async def B1(message: types.Message):
    # выполнение первого задания
    if message.text == 'Ходить на клетку E3':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Задача с полом')
        markup = types.ReplyKeyboardRemove()
        await message.answer('Постой, перед тем как сделать ход выполни задание: Пол комнаты, имеющей форму прямоугольника со сторонами 7 м и 9 м, требуется покрыть паркетом из прямоугольных дощечек со сторонами 10 см и 20 см. Сколько потребуется таких дощечек? Напиши только число.', reply_markup = markup)
        await StateMachine.B2.set()
    else:
        await message.answer('😔 На эту позицию нельзя ходить.')

@dp.message_handler(state=StateMachine.B2)
async def B2(message: types.Message):
    # сделаны 2 хода
    if message.text == '3150':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True).add('Сходить на H5')
        await message.answer('Пока я ждал твоего ответа на вопрос я уже сходил пешкой которая стояла на F7, а теперь стоит на F5')
        await asyncio.sleep(1)
        await message.answer_photo(types.InputFile(chessPath + '3.png'), 'Молодец. Ты решил все правильно!!! Теперь делай снова свой ход. Сейчас будешь ходить королевой, которая стоит на D1', reply_markup = markup)
        await StateMachine.B3.set()
    else:
        await message.answer('Ты ошибся. Попробуй ещё раз.')

@dp.message_handler(state=StateMachine.B3)
async def B3(message: types.Message):
    # сделать ход королевой
    if message.text == 'Сходить на H5':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Задача с килограммом')
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True).add('Вата', 'Железо', 'Они равны')
        await message.answer('Хорошо, для того что бы сделать ход нужно решить задачу. Задача: что легче: 1 кг ваты или 1 кг железа?', reply_markup = markup)
        await StateMachine.B4.set()
    else:
        await message.answer('😔 На эту позицию нельзя ходить.')

@dp.message_handler(state=StateMachine.B4)
async def B4(message: types.Message, state: FSMContext):
    # финал
    if message.text == 'Они равны':
        logging.info(f'{str(datetime.now())} - {message.from_user.id} - {message.from_user.full_name} - Закончил играть')
        markup = types.ReplyKeyboardRemove()
        await message.answer_photo(types.InputFile(chessPath + '4.png'), 'ПОЗДРАВЛЯЮ!!! Вы выиграли!!! Вы сделали шах и мат мне. Чтобы начать заново напишите /start', reply_markup=markup)
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ты ошибся. Попробуй ещё раз.')

executor.start_polling(dp, skip_updates=True)