__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import TypeVar
import json

Instancetype = TypeVar('Instancetype', bound='ChatGPTMonitor')


class ChatGPTMonitor(object):
    """
        Class that implements monitoring of training and usage cost for ChatGPT

        Static members:
        monitor_path:  Path for the monitoring dump
        ratio_tokens_words: Estimated ratio of number of tokens per word
        usage_token_cost: Cost per token for inference/usage
        training_token_cost: Cost per token for fine-tuning training

        Author: Patrick Nicolas
        Version: 0.1
    """
    monitor_path = '../monitor'
    ratio_tokens_words = 1.12
    usage_token_cost = {
        'gpt4': 0.03 * 0.001,
        'gpt-3.5-turbo': 0.002 * 0.00,
        'davinci': 0.12 * 0.001,
        'curie': 0.012 * 0.001
    }
    training_token_cost = {
        'davinci': 0.03 * 0.001,
        'curie': 0.003 * 0.001
    }

    def __init__(self, monitor_name: str, activities: {} = None):
        self.monitor_name = monitor_name
        if not activities:
            self.activities = {'cost': 0.0, 'num_tokens': 0, 'num_messages': 0}
        else:
            self.activities = activities

    @classmethod
    def build(cls, monitor_name: str) -> Instancetype:
        with open(f'{ChatGPTMonitor.monitor_path}/{monitor_name}', 'r') as f:
            content = f.read()
        activities = json.loads(content)
        return cls(monitor_name, activities)

    def update(self, num_words: int, model_type: str, activity: str):
        self.activities['cost'] += ChatGPTMonitor.__cost(num_words, model_type, activity)
        self.activities['num_tokens'] += ChatGPTMonitor.__num_tokens(num_words)
        self.activities['num_messages'] += 1
        self.activities[f'{activity}-{model_type}'] = self.activities.get(f'{activity}-{model_type}', 0) + 1

    def save(self):
        with open(f'{ChatGPTMonitor.monitor_path}/{self.monitor_name}', 'w') as f:
            f.write(json.dumps(self.activities))

    def __str__(self) -> str:
        return str(self.activities)

    @staticmethod
    def __num_tokens(num_words) -> int:
        return int(num_words * ChatGPTMonitor.ratio_tokens_words)

    @staticmethod
    def __cost(num_words: int, model_type: str, activity: str) -> float:
        num_tokens = ChatGPTMonitor.__num_tokens(num_words)
        return num_tokens* ChatGPTMonitor.training_token_cost[model_type] \
            if activity == 'training' \
            else \
            num_tokens * ChatGPTMonitor.usage_token_cost[model_type]


if __name__ == '__main__':
    chat_gpt_monitor = ChatGPTMonitor('monitor1', {})
    chat_gpt_monitor.update(23, 'gpt-3.5-turbo', 'usage')
    chat_gpt_monitor.update(29, 'gpt-3.5-turbo', 'usage')
    chat_gpt_monitor.update(193, 'davinci', 'training')

    print(str(chat_gpt_monitor))
    chat_gpt_monitor.save()
    chat_gpt_monitor = ChatGPTMonitor.build('monitor1')
    print(str(chat_gpt_monitor))
