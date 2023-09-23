# -*- coding: utf8 -*-
import logging
import asyncio
from typing import Any
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, F, Router, html
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
import datetime
import time
import sys
import pyowm
from pyowm.utils.config import get_default_config
import requests
from bs4 import BeautifulSoup
from translate import Translator
import random
from recipe import five_recipe
import os
#import speech_recognition as sr
import uuid
import copy
from config import TOKEN, TOKEN_OWM, admin, output_day, sunday_day, new_employee,route_54_home_sunday,route_54_city_sunday,route_53_home_sunday,route_53_city_sunday,route_52_home_sunday,route_52_city_sunday,route_51_home_sunday,route_51_city_sunday,route_54_home_saturday,route_54_city_saturday,route_53_home_saturday,route_53_city_saturday,route_52_home_saturday,route_52_city_saturday,route_51_home_saturday,route_51_city_saturday,route_51_city_weekdays,route_52_city_weekdays,route_53_city_weekdays,route_54_city_weekdays,route_51_home_weekdays,route_52_home_weekdays,route_53_home_weekdays,route_54_home_weekdays,route_30_home_weekdays, route_30_city_weekdays, route_30a_home_weekdays, route_30a_city_weekdays,route_47_home_weekdays,route_47_city_weekdays,route_30_home_saturday,route_30_city_saturday,route_30a_home_saturday,route_30a_city_saturday,route_47_home_saturday, route_47_city_saturday, route_30_home_sunday, route_30_city_sunday,route_30a_home_sunday, route_30a_city_sunday, route_47_home_sunday, route_47_city_sunday, path_to_log
from config import route_102m_home_weekdays, route_102m_home_saturday, route_102m_home_sunday, route_102m_city_weekdays, route_102m_city_saturday, route_102m_city_sunday, path_to_log
from key import markup_main, markup_admin, markup_zodiac_ru, markup_zodiac_en, markup_games, markup_102m

while True:
    try:

        owm = pyowm.OWM(TOKEN_OWM)
        form_router = Router()
        TOKEN = TOKEN
        dp = Dispatcher(storage=MemoryStorage())
        logger = logging.getLogger(__name__)
        language = 'ru_RU'
        # r = sr.Recognizer()

        class Form(StatesGroup):
            Text_employee = State()
            Choice = State()
            Cow_bull_num = State()


        async def we(message):
            start_time = time.time()
            current = datetime.datetime.now().date()
            previous_data = datetime.date(2020, 6, 26)
            print(type(previous_data), type(current), previous_data, current, type(datetime.datetime.now()), datetime.datetime.now(), type(datetime.date(2020, 6, 26)), datetime.date(2020, 6, 26))
            we_data = (current - previous_data)
            print(we_data.days)
            day = 17 - int(datetime.datetime.now().strftime("%d"))
            if day < 0:
                day = 26 - int(datetime.datetime.now().strftime("%d"))
            if day < 0:
                day = 31 - int(datetime.datetime.now().strftime("%d")) + 17
            await message.answer(f'Вы вместе уже:\n\nДней: {int(we_data.days)}\nМесяцев: {int(we_data.days/30)}\nЛет: {int(we_data.days/365)}\n{50*"-"}\nДо ближайшего праздника: {day}')
            await logir('we', start_time, message)


        async def recipe(message):
            start_time = time.time()
            await message.answer(f"{five_recipe}")
            await logir('recipe', start_time, message)


        # Обработка голосовых сообщений и перевод их на английский язык
        # async def recognise(filename, message):
        #     start_time = time.time()
        #     with sr.AudioFile(filename) as source:
        #         audio_text = r.listen(source)
        #         translator = Translator(from_lang='ru', to_lang='en')
        #         await logir('recognise', start_time, message)
        #         try:
        #             text = r.recognize_google(audio_text, language=language)
        #             print(text)
        #             return translator.translate(str(text))
        #         except:
        #             print('Sorry')
        #             return 'Sorry'

        #Формирование списка игры
        async def games_array_num_bot(message: Message, state: FSMContext):
            start_time = time.time()
            array_num_bot = []
            while len(array_num_bot) < 4:
                num = random.randint(1, 9)
                if num not in array_num_bot:
                    array_num_bot.append(num)
            await state.update_data(Cow_bull_num=array_num_bot)
            await logir('games_array_num_bot', start_time, message)


        async def get_horoscope_by_day(zodiac_sign: int, flag, message):
            res = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign={zodiac_sign}&laDate=")
            soup = BeautifulSoup(res.content, 'html.parser')
            data = soup.find('div', attrs={'class': 'main-horoscope'})
            translator = Translator(from_lang='en', to_lang='ru')
            if flag == 'ru':
                return translator.translate(str(data.p.text))
            else:
                return data.p.text

        #Отслеживание действий пользователя
        async def logir(function,start_time,message):
            f = open(path_to_log,'a')
            f.write(f'{datetime.datetime.now().date().strftime("%d.%m.%y")};{datetime.datetime.now().time().strftime("%H:%M")};{message.from_user.id};{function};{str(time.time() - start_time)[0:5]}\n')
            f.close()

        #Для удаленной выгрузки
        async def log_file(message):
            start_time = time.time()
            await message.answer_document(FSInputFile(path_to_log))
            await logir('log_file',start_time,message)

        #Чтобы бот не отключился
        async def not_sleep(message: Message):
            flag = True
            while flag:
                employee = f'\n'
                for i in new_employee:
                    employee = f'{employee}{i}\n'
                await message.answer(f'{message.from_user.id}, я пока работаю))\nКол-во условно пользователей: {len(new_employee)}\n{50*"-"}\nНовые пользователи: {employee}')
                await asyncio.sleep(450)

        async def weather(message: Message):
            try:
                start_time = time.time()
                config_dict = get_default_config()
                config_dict['language'] = 'RU'
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place('Belgorod')
                w = observation.weather
                temp = w.temperature('celsius')['temp']
                Wind = w.wind()
                # Формула для определения эффективной температуры по госту
                effective_temp = 13.12 + 0.6215 * temp - 11.37 * ((1.5 * Wind["speed"]) ** 0.16) + 0.3965 * temp * ((1.5 * Wind["speed"]) ** 0.16)
                effective_temp = round(effective_temp, 1)
                Feeling_weather = 'Ощущается как ' + str(effective_temp) + '°C'
                await message.answer('На улице сейчас ' + str(w.detailed_status) + '\n🌡Температура сейчас в районе ' + str(
                    int(temp)) + ' °C\n' + '🌬Скорость ветра = ' + str(Wind['speed']) + ' м/с\n' + str(Feeling_weather))
                await logir('weather', start_time, message)
            except:
                await message.answer('Нет связи с погодой!')

        #Получение текущей даты и времени
        async def current_datetime_today(message: Message):
            start_time = time.time()
            offset = datetime.timedelta(hours=3)
            tz = datetime.timezone(offset, name='МСК')
            current = datetime.datetime.now(tz = tz)
            current_date = current.strftime("%d.%m.%y")
            current_time = current.strftime("%H:%M")
            current_day = current.isocalendar()[2]
            current_second = 3600*int(current.strftime("%H"))+60*int(current.strftime("%M"))
            await logir('current_datetime_today', start_time, message)
            return current_date, current_time, current_day, current_second


        #Определение предыдущего рейса
        async def flight(route, current_second, flag, message: Message): 
            start_time = time.time()

            route_array = []
            for i in route:
                if flag == 'previous':
                    sing = '<'
                else:
                    sing = '>='
                if eval(f'{i} {sing} {current_second}'):
                    route_array.append(i)
            await logir('flight', start_time, message)

            if len(route_array) > 0 and flag == 'previous':
                return datetime.timedelta(seconds = route_array[-1])
            elif len(route_array) > 0 and flag == 'current':
                return datetime.timedelta(seconds = route_array[0])
            elif flag == 'next' and 1 < len(route_array):
                return datetime.timedelta(seconds = route_array[1])
            else:
                return 'Конец'


        #формирование трех рейсов
        async def schedule_route(route, message: Message):
            start_time = time.time()
            current_datetime = await current_datetime_today(message)
            previous_route = await flight(route, current_datetime[3],'previous', message)
            current_route = await flight(route, current_datetime[3],'current', message)
            next_route = await flight(route, current_datetime[3],'next', message)
            await logir('schedule_route', start_time, message)
            return previous_route, current_route, next_route


        #Вывод расписания
        async def display_schedule_route(route, message: Message):
            start_time = time.time()
            current_datetime = await current_datetime_today(message)
            if current_datetime[2] != 6 and current_datetime[2] != 7 and current_datetime[0] not in output_day:
                week = 'weekdays'
            elif (current_datetime[2] == 6 and current_datetime[0] not in output_day) or (current_datetime[0] in sunday_day):
                week = 'saturday'
            else:
                week = 'sunday'
            #print(globals().get(f'route_30_{route}_{week}'))
            M30 = await schedule_route(globals().get(f'route_30_{route}_{week}'), message)
            #M30a = await schedule_route(globals().get(f'route_30a_{route}_{week}'), message)
            M47 = await schedule_route(globals().get(f'route_47_{route}_{week}'), message)
            M51 = await schedule_route(globals().get(f'route_51_{route}_{week}'), message)
            M52 = await schedule_route(globals().get(f'route_52_{route}_{week}'), message)
            M53 = await schedule_route(globals().get(f'route_53_{route}_{week}'), message)
            M54 = await schedule_route(globals().get(f'route_54_{route}_{week}'), message)
            if route == 'city':
                await message.answer(f'<b>🚂 С ЖД вокзала:</b>\n<b>🚌 Автобус</b> №30\n<b>🔙Предыдущий - </b>{str(M30[0])[:5]} \n <b>⌚ Время отправления</b> - {str(M30[1])[:5]}\n<b>🔜Следующий - </b>{str(M30[2])[:5]}\n\n'
                                     f'<b>🚎 Автобус</b> №51\n<b>🔙Предыдущий -</b>{str(M51[0])[:5]} \n <b>⌚ Время отправления</b> - {str(M51[1])[:5]}\n<b>🔜Следующий -</b> {str(M51[2])[:5]} \n\n'
                                     f'<b>🚎 Автобус</b> №52\n<b>🔙Предыдущий -</b>{str(M52[0])[:5]} \n <b>⌚ Время отправления</b> - {str(M52[1])[:5]}\n<b>🔜Следующий -</b> {str(M52[2])[:5]} \n\n'
                                     f'<b>✈ С Аэропорта:</b>\n<b>🚌 Автобус</b> №53\n<b>🔙Предыдущий - </b>{str(M53[0])[:5]} \n <b>⌚ Время отправления</b> - {str(M53[1])[:5]}\n<b>🔜Следующий - </b>{str(M54[2])[:5]}\n\n'
                                     f'<b>🚎 Автобус</b> №54\n<b>🔙Предыдущий -</b>{str(M54[0])[:5]} \n <b>⌚ Время отправления</b> - {str(M54[1])[:5]}\n<b>🔜Следующий -</b> {str(M54[2])[:5]} \n\n'
                                                 f'<b>🏪 С Cпутника:</b>\n<b>🚍 Автобус</b> №147\n<b>🔙Предыдущий - </b>{str(M47[0])[:5]} \n<b>⌚ Время отправления</b> - {str(M47[1])[:5]}\n<b>🔜Следующий - </b>{str(M47[2])[:5]} ',
                                                 parse_mode='html')
            else:
                await message.answer(f'<b>🏛 С каштановой:</b>\n<b>🚌 Автобус</b> №30 (ЖД)\n<b>⌚️Время отправления</b> - {str(M30[1])[:5]}\n<b>🔜Следующий -</b> {str(M30[2])[:5]}\n\n'
                                     f'<b>🚎 Автобус</b> №51 (ЖД)\n<b>⌚️Время отправления</b> - {str(M51[1])[:5]}\n<b>🔜Следующий -</b> {str(M51[2])[:5]}\n\n'
                                     f'<b>🚎 Автобус</b> №52 (ЖД)\n<b>⌚️Время отправления</b> - {str(M52[1])[:5]}\n<b>🔜Следующий -</b> {str(M52[2])[:5]}\n\n'
                                     f'<b>🚎 Автобус</b> №53 (Аэр)\n<b>⌚️Время отправления</b> - {str(M53[1])[:5]}\n<b>🔜Следующий -</b> {str(M53[2])[:5]}\n\n'
                                     f'<b>🚎 Автобус</b> №54 (Аэр)\n<b>⌚️Время отправления</b> - {str(M54[1])[:5]}\n<b>🔜Следующий -</b> {str(M54[2])[:5]}\n\n'
                                                 f'<b>🚎 Автобус</b> №147 (Гора)\n<b>⌚️Время отправления</b> - {str(M47[1])[:5]} \n<b>🔜Следующий -</b> {str(M47[2])[:5]}',
                                                 parse_mode='html')
            await logir('display_schedule_route',start_time, message)

        #Вывод расписание для 102m f
        async def display_schedule_route_102m(route, message: Message):
            start_time = time.time()
            current_datetime = await current_datetime_today(message)
            if current_datetime[2] != 6 and current_datetime[2] != 7 and current_datetime[0] not in output_day:
                week = 'weekdays'
            elif (current_datetime[2] == 6 and current_datetime[0] not in output_day) or (current_datetime[0] in sunday_day):
                week = 'saturday'
            else:
                week = 'sunday'
            #print(globals().get(f'route_30_{route}_{week}'))
            M102M = await schedule_route(globals().get(f'route_102m_{route}_{week}'), message)

            if route == 'city':
                await message.answer(f'<b>🚂 С Энергомаша:</b>\n<b>🚌 Автобус</b> №102м\n<b>🔙Предыдущий - </b>{str(M102M[0])[:5]} \n<b>⌚ Время отправления</b> - {str(M102M[1])[:5]}\n<b>🔜Следующий - </b>{str(M102M[2])[:5]}\n\n',
                                                 parse_mode='html')
            else:
                await message.answer(f'<b>🏛 С пр-т Славы:</b>\n<b>🚌 Автобус</b> №102м \n<b>⌚️Время отправления</b> - {str(M102M[1])[:5]}\n<b>🔜Следующий -</b> {str(M102M[2])[:5]}\n\n',
                                                 parse_mode='html')
            await logir('display_schedule_route',start_time, message)

        #Выгрузка log_file
        async def log_file(path, message):
            start_time = time.time()
            await message.answer_document(FSInputFile(path))
            await logir('log_file', start_time, message)

        async def delivery_sms(id_recipient,id_sunder,text,message: Message):
            start_time = time.time()
            bot = Bot(TOKEN, parse_mode = "html")
            await bot.send_message(id_recipient, f'Сообщение от: <a href="tg://user?id={int(id_sunder)}">{str(message.from_user.first_name)}</a>\nТехт: {text}', reply_markup = markup_main)
            await message.answer('Сообщение отправлено!')
            await bot.session.close()
            await logir('delivery_sms',start_time, message)

        async def games(message):
            array_num = []
            while len(array_num) < 4:
                num = random.randint(1,9)
                if num not in array_num:
                    array_num.append(num)
            print(array_num)

        @form_router.callback_query(lambda c: c.data)
        async def call_handle(call: types.callback_query, state: FSMContext) -> None:
            if int(call.data) < 14 :
                await call.message.edit_text(await get_horoscope_by_day(call.data, 'ru' ,call))
            else:
                zod = int(call.data) - 100
                await call.message.edit_text(await get_horoscope_by_day(zod, 'en', call))

        # Обработка голосовых сообщений и перевод их на английский язык
        # @form_router.message(content_types=['voice'])
        # async def voice_processing(message):
        #     start_time = time.time()
        #     bot = Bot(TOKEN, parse_mode="html")
        #     filename = str(uuid.uuid4())
        #     file_name_full = "./voice" + filename + ".ogg"
        #     file_name_full_converted = "./ready/" + filename + ".wav"
        #     file_info = await bot.get_file(message.voice.file_id)
        #     downloaded_file = await bot.download_file(file_info.file_path)
        #     with open(file_name_full, 'wb') as new_file:
        #         new_file.write(downloaded_file)
        #     os.system("ffmpeg -i " + file_name_full + " " + file_name_full_converted)
        #     text = recognise(file_name_full_converted, message)
        #     await bot.reply_to(text)
        #     os.remove(file_name_full)
        #     os.remove(file_name_full_converted)
        #     await bot.session_close()
        #     await logir('voice_processing', start_time, message)

        # Процесс игры
        @form_router.message(Form.Choice)
        async def games(message: Message, state: FSMContext):
            start_time = time.time()
            array_game_user = []
            array_bot = await state.get_data()
            array_num_user = [message.text[i] for i in range(0, len(message.text))]
            array_game = copy.deepcopy(array_num_user)
            array_game_bot = copy.deepcopy(array_bot['Cow_bull_num'])
            print(array_game_bot)
            for i in array_game:
                array_game_user.append(int(i))
            num_accurate = [i for i, j in zip(array_game_user, array_game_bot) if i == j]
            print(num_accurate)
            for num in num_accurate:
                array_game_user.remove(num)
                array_game_bot.remove(num)
            num_inaccurate = list(set(array_game_user).intersection(array_game_bot))
            print(num_inaccurate, num_accurate)
            if len(num_accurate) < 4:
                await state.set_state(Form.Choice)
                await message.answer(
                    f"Твой вариант: {message.text}\n{len(num_accurate)} {'быка' if len(num_accurate) > 1 else 'быков'} и {len(num_inaccurate)} {'коров' if len(num_inaccurate) == 0 else ('коровы' if len(num_inaccurate) != 1 else 'корова' )}.\nПопробуй еще раз)")
            else:
                await state.clear()
                await message.answer(f"МУУУ, ты нашел всех быков, поздравляю!!!", reply_markup=markup_main)
            await logir('games', start_time, message)

        @form_router.message(Form.Text_employee)
        async def help_text(message: Message, state: FSMContext):
            start_time = time.time()
            try:

                id = message.from_user.id
                if id in admin:
                    text = message.text.split(',')
                    await delivery_sms(text[0], admin[0], text[1], message)
                else:
                    text = message.text
                    await delivery_sms(admin[0], id, text, message)
                await state.clear()
                await logir('help_text', start_time, message)
            except:
                await state.clear()
                await message.answer('Ошибка. Попробуй сначала.')


        @form_router.message(commands={"cancel"})
        @form_router.message(F.text.casefold() == "cancel")
        async def cancel_handler(message: Message, state: FSMContext) -> None:
            """
            Allow user to cancel any action
            """
            current_state = await state.get_state()
            if current_state is None:
                return

            logging.info("Cancelling state %r", current_state)
            await state.clear()
            await message.answer(
                "Операция отменена.",
                reply_markup=markup_main,
            )

        #Поддержка
        @form_router.message(commands={"help"})
        async def help_user(message: Message, state: FSMContext):
            start_time = time.time()
            await state.set_state(Form.Text_employee)
            await message.answer('Напиши свой вопрос.\nЯ передам его в поддержку.\nЕсли передумаешь, то введи /cancel',reply_markup = markup_main)
            await logir('help_user',start_time, message)

        #Переход в режим админ
        @form_router.message(commands={"admin"})
        async def key(message: Message):
            start_time = time.time()
            await message.answer('Ты в режиме администратора',reply_markup = markup_admin)
            await logir('admin',start_time, message)

        #Починка клавиатуры
        @form_router.message(commands={"key"})
        async def key(message: Message):
            start_time = time.time()
            await message.answer('Я починиль',reply_markup = markup_main)
            await logir('key',start_time, message)

        #Клавиатура для майского 102м
        @form_router.message(commands={"102m"})
        async def key(message: Message):
            start_time = time.time()
            await message.answer('Вы выбрали клавиатуру для направления Майский',reply_markup = markup_102m)
            await logir('key',start_time, message)

        #Действие при запуске бота
        @form_router.message(commands={"start"})
        async def start(message: Message):
            start_time = time.time()
            new_employee.append(f'{message.from_user.id}')
            await message.reply_sticker("CAACAgIAAxkBAAEOeXNiI10x4eG7LXSdRWogN8wTp5ezdAAC_RIAAk89GEvo1GtuJXMfbyME")
            await message.answer('Здравствуй. Куда ты хочешь отправиться? Выбери необходимый путь на клавиатуре. \nЕсли когда-нибудь клавитаруа сломается, то введи /key\nЕсли захочешь написать в поддержку, то введи /help',reply_markup = markup_main)
            await logir('start',start_time, message)

        @form_router.message(content_types=['text'])
        async def text_button(message: Message, state: FSMContext):
            if message.text == '🏫 В город':
                start_time = time.time()
                await display_schedule_route('home',message)
                await logir('Домой',start_time, message)
            elif message.text == '🏠 Домой':
                start_time = time.time()
                await display_schedule_route('city',message)
                await logir('В городе',start_time, message)
            elif message.text == 'ГО':
                await not_sleep(message)
            elif message.text == 'Hi':
                await state.set_state(Form.Text_employee)
                await message.answer('Введите id и текст получателя.\nПример: 11, Привет')
            elif message.text == '⛅ Погода':
                await weather(message)
            elif message.text == '🔮 Гороскоп':
                await message.answer('Выбери знак зодиака (RU).\nНажми один раз и жди!', reply_markup = markup_zodiac_ru)
                await message.answer('Выбери знак зодиака (EN).\nНажми один раз и жди!', reply_markup= markup_zodiac_en)
            elif message.text == path_to_log:
                await log_file(message)
            elif message.text == 'Рецепт':
                start_time = time.time()
                await recipe(message)
                await logir('Рецепт', start_time, message)
            elif message.text == 'Вместе':
                start_time = time.time()
                await we(message)
                await logir('Вместе', start_time, message)
            elif message.text == '$':
                start_time = time.time()
                value_d = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()['Valute']['USD']['Value']
                await message.answer(f"Cейчас 1 доллар это {value_d} рубля")
                await logir('USD', start_time, message)
            elif message.text == '€':
                start_time = time.time()
                value_d = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()['Valute']['EUR']['Value']
                await message.answer(f"Cейчас 1 евро это {value_d} рубля")
                await logir('EUR', start_time, message)
            elif message.text == 'Новая игра':
                start_time = time.time()
                await games_array_num_bot(message, state)
                await state.set_state(Form.Choice)
                await message.answer(
                    'Я придумал! Введи 4-х значное число с неповторяющимися цифрами.\nБыки - угадал цифру и ее расположение. Корова - угадал только цифру.\nЕсли надоест играть, нажми на клавиатуре кнопку "/cancel".',
                    reply_markup=markup_games)
                await logir('Игра', start_time, message)
            elif message.text == '🏠 Домой (102м)':
                start_time = time.time()
                await display_schedule_route_102m('city', message)
                await logir('Домой', start_time, message)
            elif message.text == '🏫 В город (102м)':
                start_time = time.time()
                await display_schedule_route_102m('home', message)
                await logir('В городе', start_time, message)
            elif message.text == '?':
                yes_no = 'да' if random.randint(1, 2) == 1 else 'не'
                await message.answer(f"Я тебе говорю {yes_no} делай это!")
                await message.answer(f"Он уже мчииит под цифрой {random.randint(1, 10)}")
            elif message.text == path_to_log:
                start_time = time.time()
                await log_file(path_to_log,message)
                await logir(f'{path_to_log}', start_time, message)
            else:
                await message.answer('Не понимать((\nЕсли введешь "Новая игра", то сможешь поиграть в игру) ')



        def main() -> None:
            dp.include_router(form_router)
            bot = Bot(TOKEN, parse_mode="html")
            # And the run events dispatching
            dp.run_polling(bot)


        if __name__ == "__main__":
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            asyncio.run(main())
    except:
        pass
