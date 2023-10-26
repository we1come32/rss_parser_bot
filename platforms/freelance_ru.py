import requests
from bs4 import BeautifulSoup
from loguru import logger

from platforms.base import Platform, Task


class Freelance_ru(Platform):
    base_url = "https://freelance.ru/project/search/pro?q=python"

    @logger.catch(default=[])
    def parse(self) -> list[Task]:
        html = BeautifulSoup(requests.get(self.base_url).text, 'html.parser')
        tasks = []
        for project in html.find_all(attrs={"class": "project"}):
            if project.text:
                continue
            tasks.append(Task(
                title=project.find(attrs={"class": "title"}).text.strip(),
                description=project.find(attrs={"class": "description"}).text.strip(),
                themes=project.find(attrs={"class": "specs-list"}).text.strip().replace(
                    "  ", "").replace("\n", "; ")[:1000],
                price=project.find(attrs={"class": "cost"}).text.strip(),
                limit_time=project.find(attrs={"class": "term"}).text.strip(),
                published_date=project.find(
                    attrs={"class": "publish-time"}).text.strip().replace("  ", "").replace("\n", " "),
                author=project.find(attrs={"class": "user-name"}).text.strip(),
                href="https://freelance.ru"+project.find(attrs={"class": "description"}).attrs['href'],
            ))
        return tasks
