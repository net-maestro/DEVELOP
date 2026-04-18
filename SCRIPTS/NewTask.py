# -*- coding: utf-8 -*-
import os
import re
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import pymysql.cursors

from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Configuration
bot_token = os.getenv('TASK_BOT_TOKEN')
chat_id = os.getenv('TASK_CHAT_ID')

database_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8',
}

bot = telebot.TeleBot(token=bot_token)

def get_html_symbol(reason):
    # Словарь с причинами и их соответствующими HTML символами
    reason_symbols = {
    'Підключення інтернету': '&#9989;',              # ✅
    'Підключення оптоволокна': '&#9989;',           # ✅
    'Тимчасове відключення': '&#128683;',           # 🚫
    'Розірвання договору': '&#128465;',             # 🗑️
    'Повторна активація': '&#128472;',              # 🛠️
    'Інше': '&#10067;',                             # ❓
    'Ремонт': '&#128295;',                          # 🔧
    'Призупинення послуги через борг': '&#128276;', # 🔒
    'Заявка ЛК': '&#128221;',                       # 📝
    'Заявка Сайт/Telegram': '&#128233;',            # 📨
    'Перевірка оплати': '&#128176;',                # 💰
    'Видача ключа': '&#128273;',                    # 🔑
    'Консультація': '&#128172;',                    # 💬
    'Підключення аудіодомофону': '&#127908;',       # 🎤
    'Підключення відеодомофону': '&#128249;',       # 📹
    'Налаштування IPTV': '&#128250;',               # 📺
    'Будівництво': '&#128738;',                     # 🏗️
    'Нарахування бонусів': '&#127873;'              # 🎁
     }

    # Возвращаем HTML символ по причине или сообщение об ошибке
    return reason_symbols.get(reason, 'Причина не знайдена')
def format_date(date):
    # Форматирование в нужный формат
    formatted_date = date.strftime("%d.%m.%Y")
    return(formatted_date)


def create_button(current_date):
    date = format_date(current_date)
    LINK_QUESTION_ALL = f'''https://service.happylink.net.ua/abonents/questions?agreement=&reason=-1&type_date=1&date1={date}&date2={date}&responsible=-1&closed_by=-1&city=0&street=0&house=0&action=sear>
    # Создание инлайн-кнопки с короткой ссылкой
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Всі заявки", url=LINK_QUESTION_ALL)
    return(markup.add(button))




def get_latest_question(conn):
    query = '''
        SELECT q.created, e.`name` AS created_employee, q.reason, s.agreement,
               CONCAT('г.', c.name, ', ', st.name, ', д.', h.`name`, ', под.', s.entrance, ', эт.', s.floor, ', кв.', s.apartment) AS addr,
               q.phone, q.`comment`, q.dest_time, re.name AS responsible_employee, e.telegram_id, q.is_sent_tg, q.id
        FROM questions_full q
        JOIN clients s ON q.agreement = s.id
        JOIN addr_houses h ON h.id = s.house
        JOIN addr_streets st ON st.id = h.street
        JOIN addr_cities c ON c.id = st.city
        LEFT JOIN employees e ON e.id = q.created_employee
        LEFT JOIN employees re ON re.id = q.responsible_employee
        WHERE CAST(q.dest_time AS date) = CAST(NOW() AS date)
        ORDER BY q.created DESC
        LIMIT 1
    '''
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()


def format_message(data):
    agreement_number = data[3]
    agreement_link = f'https://provider.net.ua/abonents/detail?agreement={agreement_number}'
    formatted_number = re.sub(r'\D', '', data[5])[2:]

    def is_employee():
        if data[8] == None:
            return ''
        else:
            EMPLOYEE =  f'<b>Виконавець:</b> {data[8]}'
            return(EMPLOYEE)
    EM = is_employee()

    def not_send_address():
        value = str(data[4]).strip()
        if not value or value == "777":
            return ''
        return f"<b>Адреса:</b> {value}\n"

    ADDRESS = not_send_address()



    return (
        f"<b>Створена:</b> {data[0].strftime('%m/%d/%Y, %H:%M:%S')}\n"
        f"👤 {data[1]}\n"
        f"<b>Причина:</b> {data[2]} {get_html_symbol(data[2])}\n"
        f"<b>Договір:</b> <a href='{agreement_link}'>{agreement_number}</a>\n"
        f"{ADDRESS}"
        f"📞 <a href='tel:{formatted_number}'>{formatted_number}</a>\n"
        f"<b>Коментар:</b> " + data[6].replace('\n', '\n> ') + "\n"
        f"<b>Призначено:</b> 🕒 {data[7].strftime('%m/%d/%Y, %H:%M:%S')}\n"
        f"{EM}"
    )


def send_telegram_message(bot, chat_id, message, button):
    try:
        bot.send_message(chat_id, message, reply_markup=button, parse_mode='HTML')
        print("Message sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the photo: {e}")

def update_question_status(conn, question_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE questions SET is_sent_tg='YES' WHERE id={question_id}")
        conn.commit()
        print(f"Record with id={question_id} updated successfully.")
    except Exception as e:
        print(f"An error occurred during UPDATE: {e}")

def main():
    t = datetime.now().strftime("%m/%d/%Y, %H:%M")

    with pymysql.connect(**database_config) as conn:
        data = get_latest_question(conn)
        print(format_date(data[7]))

        if data and data[10] == 'NO':  # Check if is_sent_tg is 'NO'
            message = format_message(data)
            button = create_button(data[7])
            send_telegram_message(bot, chat_id, message, button)
            update_question_status(conn, data[11])

if __name__ == "__main__":
    main()
