from deque import *
from collections import deque


class TeamMember:
    def __init__(self, name, duty):
        self.name = name
        self.duty = duty
        self.tasks = deque()

    def addTask(self, title, description, priority):
        task = DequeNode(title, description, priority)
        self.tasks.append(task)

    def removeTask(self, task_title):
        for task in list(self.tasks):
            if task_title == task_title:
                self.tasks.remove(task)
