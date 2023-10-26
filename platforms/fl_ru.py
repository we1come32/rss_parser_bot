import requests
from bs4 import BeautifulSoup
from loguru import logger
from fake_useragent import UserAgent

from platforms.base import Platform, Task


class Fl_ru(Platform):
    urls = [
        "https://www.fl.ru/rss/projects.xml?subcategory=279&category=5",  # Боты
    ]

    def __init__(self):
        super().__init__()

        ua = UserAgent()
        fake_headers = {'user-agent': ua.random.strip()}
        self.session = requests.session()
        self.session.headers.update(fake_headers)

    @staticmethod
    def format_str(string: str):
        if string.startswith('<![CDATA['):
            string = string[9:]
        if string.endswith(']]>'):
            string = string[:-3]
        return string

    @logger.catch(default=[])
    def parse(self) -> list[Task]:
        tasks = []
        for url in self.urls:
            xml = self.session.get(url)
            html = BeautifulSoup(xml.text, 'html.parser')
            for project in html.find_all('item'):
                # print(project)
                tasks.append(task := Task(
                    title=self.format_str(project.find('title').text.strip()),
                    description=self.format_str(project.find('description').text.strip()),
                    themes=self.format_str(project.find('category').text.strip()),
                    price='В заказе',
                    limit_time='В заказе',
                    published_date=self.format_str(project.find('pubdate').text.strip()),
                    author="Неизвестно",
                    href=project.find('guid').text,
                ))
                # print(task)
        return tasks
