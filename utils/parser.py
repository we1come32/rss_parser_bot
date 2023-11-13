import time
from asyncio import sleep
from datetime import datetime
from typing import List

import feedparser
import httpx as httpx
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    published_date: datetime
    link: str
    tags: List[str]


async def parse(url: str, httpx_client: httpx.AsyncClient = None):
    if httpx_client is None:
        httpx_client = httpx.AsyncClient()

    try:
        response = await httpx_client.get(url)
    except:
        return

    feeds = feedparser.parse(response.text)
    for entry in feeds['entries']:
        date: time.struct_time = entry.get('published_parsed', '')
        yield Task(
            title=entry.get('title', ''),
            description=entry.get('summary', ''),
            published_date=datetime(
                year=date.tm_year,
                month=date.tm_mon,
                day=date.tm_mday,
                hour=date.tm_hour,
                minute=date.tm_min,
                second=date.tm_sec,
                tzinfo=date.tm_zone
            ),
            link=entry.get('link', ''),
            tags=[tag['term'] for tag in entry.get('tags', [])],
        )
