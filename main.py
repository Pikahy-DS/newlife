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


from config import TOKEN, TOKEN_OWM, admin, output_day, new_employee, route_30_home_weekdays, route_30_city_weekdays, route_30a_home_weekdays, route_30a_city_weekdays,route_47_home_weekdays,route_47_city_weekdays,route_30_home_saturday,route_30_city_saturday,route_30a_home_saturday,route_30a_city_saturday,route_47_home_saturday, route_47_city_saturday, route_30_home_sunday, route_30_home_sunday,route_30a_home_sunday, route_30a_city_sunday, route_47_home_sunday, route_47_city_sunday, path_to_log
from key import markup_main, markup_admin, markup_zodiac_ru, markup_zodiac_en

while True:
    try:
        owm = pyowm.OWM(TOKEN_OWM)
        form_router = Router()
        TOKEN = TOKEN
        dp = Dispatcher(storage=MemoryStorage())
        logger = logging.getLogger(__name__)

        class Form(StatesGroup):
            Text_employee = State()


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
                observation = mgr.weather_at_place('Старый Оскол')
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
            current = datetime.datetime.now()
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
            if len(route_array) > 0 and (flag == 'previous' or flag == 'current'):
                return datetime.timedelta(seconds = route_array[-1])
            elif flag == 'next' and len(route) <= len(route_array)+1:
                return datetime.timedelta(seconds = route[len(route_array)+1])
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
            elif current_datetime[2] == 6 and current_datetime[0] not in output_day:
                week = 'saturday'
            else:
                week = 'sunday'
            M30 = await schedule_route(globals().get(f'route_30_{route}_{week}'), message)
            M30a = await schedule_route(globals().get(f'route_30a_{route}_{week}'), message)
            M47 = await schedule_route(globals().get(f'route_47_{route}_{week}'), message)
            if route == 'city':
                await message.answer(f'<b>🚂 С ЖД вокзала:</b>\n<b>🚌 Автобус</b> №30\n<b>🔙Предыдущий -</b>{str(M30[0])[:5]} \n <b>⌚ Время отправления</b> - {str(M30[1])[:5]}\n<b>🔜Следующий - </b>{str(M30[2])[:5]}\n\n<b>🚎 Автобус</b> №30A\n<b>🔙Предыдущий -</b>{str(M30a[0])[:5]} \n <b>⌚ Время отправления</b> - {str(M30a[1])[:5]}\n<b>🔜Следующий -</b> {str(M30a[2])[:5]} \n\n<b>🏪 С Cпутника:</b>   '
                                                 f'\n<b>🚍 Автобус</b> №47\n<b>🔙Предыдущий -</b>{str(M47[0])[:5]} \n<b>⌚ Время отправления</b> - {str(M47[1])[:5]}\n<b>🔜Следующий - </b>{str(M47[2])[:5]} ',
                                                 parse_mode='html')
            else:
                await message.answer(f'<b>🏛 С каштановой:</b>\n<b>🚌 Автобус</b> №30\n<b>⌚️Время отправления</b> - {str(M30[1])[:5]}\n<b>🔜Следующий -</b> {str(M30[2])[:5]}\n\n<b>🚎 Автобус</b> №30A\n<b>⌚️Время отправления</b> - {str(M30a[1])[:5]}\n<b>🔜Следующий -</b> {str(M30a[2])[:5]}\n'
                                                 f'\n<b>🚎 Автобус</b> №47\n<b>⌚️Время отправления</b> - {str(M47[1])[:5]} \n<b>🔜Следующий -</b> {str(M47[2])[:5]}',
                                                 parse_mode='html')
            await logir('display_schedule_route',start_time, message)

        async def delivery_sms(id_recipient,id_sunder,text,message: Message):
            start_time = time.time()
            bot = Bot(TOKEN, parse_mode = "html")
            await bot.send_message(id_recipient, f'Сообщение от: {id_sunder}\nТехт: {text}', reply_markup = markup_main)
            await message.answer('Сообщение отправлено!')
            await bot.session.close()
            await logir('delivery_sms',start_time, message)


        @form_router.callback_query(lambda c: c.data)
        async def call_handle(call: types.callback_query, state: FSMContext) -> None:
            if int(call.data) < 14 :
                await call.message.edit_text(await get_horoscope_by_day(call.data, 'ru' ,call))
            else:
                zod = int(call.data) - 100
                print(call.data)
                await call.message.edit_text(await get_horoscope_by_day(zod, 'en', call))

        @form_router.message(Form.Text_employee)
        async def help_text(message: Message, state: FSMContext):
            start_time = time.time()
            try:
                text = message.text.split(',')
            except:
                await state.clear()
                await message.answer('Ошибка. Попробуй сначала.')
            id = message.from_user.id
            if id in admin:
                await delivery_sms(text[0],admin[0],text[1],message)
            else:
                await delivery_sms(admin[0],id,text,message)
            await logir('help_text',start_time, message)

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
            else:
                await message.answer('Не понимать((')


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
