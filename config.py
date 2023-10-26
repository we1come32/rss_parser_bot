from os import getenv


bot_token = getenv('BOT_ACCESS_TOKEN')
admin_id = getenv('ADMIN_TELEGRAM_ID')
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
