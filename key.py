from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup

builder_main = [[KeyboardButton(text='🏠 Домой'), KeyboardButton(text='🏫 В город')],[KeyboardButton(text='🔮 Гороскоп'), KeyboardButton(text = '⛅ Погода')]]
markup_main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=builder_main)
builder_admin = [[KeyboardButton(text='🏠 Домой'), KeyboardButton(text='🏫 В город')],[KeyboardButton(text='Hi'), KeyboardButton(text='ГО'),  KeyboardButton(text='Новая игра')],[KeyboardButton(text='€'), KeyboardButton(text='$'),  KeyboardButton(text='Вместе'),  KeyboardButton(text='Рецепт')]]
markup_admin = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=builder_admin)

builder_zodiac_ru = [[InlineKeyboardButton(text='Овен', callback_data='1'),InlineKeyboardButton(text='Скорпион', callback_data='8'),InlineKeyboardButton(text='Близнецы', callback_data='3'),],
                  [InlineKeyboardButton(text='Рак', callback_data='4'),InlineKeyboardButton(text='Лев', callback_data='5'),InlineKeyboardButton(text='Дева', callback_data='6')],
                  [InlineKeyboardButton(text='Весы', callback_data='7'),InlineKeyboardButton(text='Телец', callback_data='2'), InlineKeyboardButton(text='Стрелец', callback_data='9')],
                  [InlineKeyboardButton(text='Козерог', callback_data='10'), InlineKeyboardButton(text='Водолей', callback_data='11'),InlineKeyboardButton(text='Рыба', callback_data='12')]]
markup_zodiac_ru = InlineKeyboardMarkup(inline_keyboard=builder_zodiac_ru)

builder_zodiac_en = [[InlineKeyboardButton(text='Aries', callback_data='101'),InlineKeyboardButton(text='Scorpio', callback_data='108'), InlineKeyboardButton(text='Gemini', callback_data='103')],
                  [InlineKeyboardButton(text='Cancer', callback_data='104'),InlineKeyboardButton(text='Leo', callback_data='105'),InlineKeyboardButton(text='Virgo', callback_data='106')],
                  [InlineKeyboardButton(text='Libra', callback_data='107'),InlineKeyboardButton(text='Taurus', callback_data='102'),InlineKeyboardButton(text='Sagittarius', callback_data='109')],
                  [InlineKeyboardButton(text='Capricorn', callback_data='110'),InlineKeyboardButton(text='Aquarius', callback_data='111'),InlineKeyboardButton(text='Pisces', callback_data='112')]]
markup_zodiac_en = InlineKeyboardMarkup(inline_keyboard=builder_zodiac_en)

builder_games = [[KeyboardButton(text = 'Новая игра')],[KeyboardButton(text='/cancel')]]
markup_games = ReplyKeyboardMarkup(resize_keyboard = True, keyboard = builder_games)