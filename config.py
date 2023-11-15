from os import getenv

from dotenv import load_dotenv


load_dotenv()


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
