import telebot
from telebot import types

import psycopg2

dbname = 'HonkaiStarRail'
user = 'postgres'
password = '3456tgh3456'
host = 'localhost'
port = '5432'

TOKEN = '6713805138:AAHyEoTI4P3reOVTQbNjXRlVCueyvVhFZe4'
bot = telebot.TeleBot(TOKEN)

conn_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'"
try:
    conn = psycopg2.connect(conn_string)
    print("Подключение к базе данных успешно установлено!!!!!")

except Exception as e:
    print("Ошибка(((((")
    print(e)

# cursor = conn.cursor()
# conn.autocommit = True
#
#
# try:
#     cursor.execute("SELECT * FROM weapon")
#     records = cursor.fetchall()
#     for record in records:
#         print(record)
# except Exception as e:
#     print("Ошибка при выполнении SQL запроса:")
#     print(e)
#
# conn.close()


# conn = psycopg2.connect(dbname='HonkaiStarRail', user='postgres', password = '3456tgh3456', host = 'localhost')


# def send_welcome(message):
#     markup = types.InlineKeyboardMarkup()
#     button_5 = types.InlineKeyboardButton('5 звезд', callback_data='star5')
#     button_4 = types.InlineKeyboardButton('4 звезд', callback_data='star4')
#     markup.add(button_5, button_4)
#     bot.send_message(message.chat.id, 'Выберете редкость персонажа:', reply_markup=markup)



@bot.message_handler(commands=['start'])
def query_handler(message):

    markup = types.InlineKeyboardMarkup()
    with conn.cursor() as cursor:
        # x=
        cursor.execute("SELECT name_character FROM character")
        for (name_character,) in cursor.fetchall():
            button = types.InlineKeyboardButton(name_character, callback_data=name_character)
            markup.add(button)
    bot.send_message(message.chat.id, "Выберете персонажа:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    character_name = call.data
    with conn.cursor() as cursor:
        cursor.execute("SELECT name_character, star_character, type_battle, way FROM character WHERE name_character = %s", (character_name,))
        character_info = cursor.fetchone()
        if character_info:
            response = f"Имя: {character_info[0]}\n Редкость: {character_info[1]}"
        else:
            response = "Информация о персонаже не найдена(("
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response)


bot.polling(none_stop=True)