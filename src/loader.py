import json
from src.task.Task import Task
from typing import List
import glob
import os
from _datetime import datetime


class JsonTaskLoader:
    @classmethod
    def load_task(cls, file_path: str) -> Task:
        with open(file_path, 'r') as file:
            data = json.load(file)
            data_begin_date = data['beginDate']
            data_finish_date = data['finishDate']
            data_deadline_date = data['deadlineDate']
            result_task = Task.create_task(
                data['name'],
                data['state'],
                data['priority'],
                data['category'],
                data['description'],
                datetime.fromisoformat(data_begin_date) if data_begin_date else None,
                datetime.fromisoformat(data_finish_date) if data_begin_date else None,
                datetime.fromisoformat(data_deadline_date) if data_begin_date else None,
                data['command']
            )
        return result_task

    @classmethod
    def load_all_tasks(cls, dir_path: str) -> List[Task]:
        result = []
        for file_path in glob.glob(dir_path + "/**", recursive=True):
            if os.path.isfile(file_path):
                result.append(cls.load_task(file_path))
        return result
