from os import getenv

from dotenv import load_dotenv


load_dotenv()

# Messages
new_task_message = """<b>Новая задача! Платформа <i>{platform}</i></b>

<b>Название</b>: <i>{title}</i>
<b>Описание</b>: <i>{description}</i>
<b>Сроки</b>: <i>{limit_time}</i>
<b>Цена</b>: <i>{price}</i>

<b>Темы</b>: <i>{themes}</i>

{published_date}. Автор: {author}
"""

short_new_task_message = """<b>Новая задача! Платформа <i>{platform}</i></b>

<b>Название</b>: <i>{title}</i>
<b>Описание</b> по ссылке ниже <i>(short msg)</i>
<b>Сроки</b>: <i>{limit_time}</i>
<b>Цена</b>: <i>{price}</i>

<b>Темы</b>: <i>{themes}</i>

{published_date}. Автор: {author}
"""


# Database section

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")

# Telegram section

BOT_TOKEN = getenv('BOT_ACCESS_TOKEN')
TG_ADMIN_ID = getenv('ADMIN_TELEGRAM_ID')

# System section

DEBUG = getenv('DEBUG', '').lower() in ['true', '1']
