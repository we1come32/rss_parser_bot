from abc import ABC, abstractmethod


class Task(dict):
    def __hash__(self):
        return hash(self['title'])

    def __gt__(self, other):
        if not isinstance(other, Task):
            return super().__gt__(other)
        return self['title'] > other['title']

    def __eq__(self, other):
        if not isinstance(other, Task):
            return super().__eq__(other)
        return self['title'] == other['title']


class Platform(ABC):
    def __init__(self, base_url: str = None):
        if base_url:
            self.base_url = base_url
        self.tasks = set()

    @abstractmethod
    def parse(self) -> list[Task]:
        pass

    def get_new_tasks(self) -> list[Task]:
        tasks = self.parse()
        new_tasks = []
        for task in tasks:
            if task not in self.tasks:
                new_tasks.append(task)
                self.tasks.add(task)
        return new_tasks
