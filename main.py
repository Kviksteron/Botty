import time
import datetime
import telebot
from pyowm.commons.exceptions import NotFoundError

import config
from pyowm import OWM

bot = telebot.TeleBot(config.TOKEN)
owm = OWM('ff84f86a51588f52d89952eb8cc61317')
mngr = owm.weather_manager()

@bot.message_handler(commands=['help'])
def help(message):
    mes = ['/start - описание',
           '/help - команды',
           '/weather - погода',
           '/joke - рассказать анекдот'
           ]
    bot.send_message(message.chat.id, '\n'.join(mes))


@bot.message_handler(commands=['start'])
def start(message):
    mes = 'удали чат пожалуйста'
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=['weather'])
def weather_call(message):
    bot.send_message(message.from_user.id, "Введите название города")
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    try:
        observation = mngr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        if temp < 0:
            bot.send_message(message.from_user.id, "🥶❄️  Бррр... Холодрыга, стоит одеться теплее.  🥶❄️")
            bot.send_message(message.from_user.id, f'В городе {message.text} сейчас {round(temp)} градусов.')
        elif 0 < temp < 10:
            bot.send_message(message.from_user.id, "☁☁  Прохладно, дольше 10 минут без куртки на улице не погуляешь.🤧 ☁☁")
            bot.send_message(message.from_user.id, f'В городе {message.text} сейчас {round(temp)} градусов.')
        elif 20 > temp > 10:
            bot.send_message(message.from_user.id, "Тепло, можно попробовать выйти из дома без куртки.  🙂😸")
            bot.send_message(message.from_user.id, f'В городе {message.text} сейчас {round(temp)} градусов.')
        elif temp > 20:
            bot.send_message(message.from_user.id, "☀☀   Жара! Можно одеться легко.   ☀☀")
            bot.send_message(message.from_user.id, f'В городе {message.text} сейчас {round(temp)} градусов.')
    except Exception:
        bot.send_message(message.from_user.id, 'Упс... Такого города не знаю, попробуй ещё раз')




bot.polling(none_stop=True, interval=0)

