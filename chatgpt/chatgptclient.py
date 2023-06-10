__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

import openai
from dataclasses import dataclass
from typing import TypeVar
from chatgpt import load_api_key

Instancetype = TypeVar('Instancetype', bound='ChatGPT')


@dataclass
class ChatGPTRequest:
    """
        Data class for the generic request to ChatGPT API
        :param Identifier of the model (i.e. gpt-3.5-turbo)
        :param role of the user {system|user|assistant}
        :param Hyper-parameter that adjusts the distribution (softmax) for the prediction of the next word/token
        :param max_tokens Limit the number of tokens used in the response
        :param top_p Sample the tokens with top_p probability.
        :param n Number of solutions/predictions
        :param presence_penalty Penalize new tokens which appear in the text so far if positive.
        :param frequency_penalty Penalize new tokens which appear in the text with higher frequency i
    """
    model: str
    user: str
    temperature: float
    max_tokens: int
    top_p: int
    n: int
    presence_penalty: int
    frequency_penalty: int

    def __str__(self):
        return f'Model: {self.model}, Role: {self.user}'


@dataclass
class ChatGPTChoice:
    text: str
    index: int
    finish_reason: str


@dataclass
class ChatGPTMessage:
    role: str
    content: str


@dataclass
class ChatGPTUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatGPTResponse:
    id: str
    object: str
    created: int
    model: int
    choices: []
    usage: ChatGPTUsage

class ChatGPTClient(object):
    import constants
    # static variable for the API key and the default maximum number of tokens returned
    openai.api_key = load_api_key()
    default_max_tokens = 256

    def __init__(self, chat_gpt_request: ChatGPTRequest):
        """
            :param chat_gpt_request fully defined request to ChatGP API
            :type chat_gpt_request ChatGPTRequest
        """
        self.chat_gpt_request = chat_gpt_request

    def __str__(self):
        return str(self.chat_gpt_request)

    @classmethod
    def build(cls, model: str, role: str, temperature: float) -> Instancetype:
        """
            Static constructor or builder for model, user and temperature request parameters and
            using all other default parameters.
            :param model: Open AI
            :param role: User or System
            :param temperature: Temperature param for the softmax function (higher value smooth choices)
            :return: Instance of the GPT client
        """
        chat_gpt_request = ChatGPTRequest(model, role, temperature, ChatGPTClient.default_max_tokens, 1, 1, 0, 0)
        return cls(chat_gpt_request)

    def post(self, prompt: str) -> (str, int):
        """
            Post a prompt/request to ChatGPT given the parameters defined in the constructor.
            It only returns the content of the message
            :param prompt: Prompt or content of the request
            :return: First choice message content
        """
        import logging
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_gpt_request.model,
                messages=[{'role': self.chat_gpt_request.user, 'content': prompt}],
                temperature=self.chat_gpt_request.temperature,
                max_tokens=self.chat_gpt_request.max_tokens
            )
            return response['choices'][0].message.content, response['usage'].total_tokens
        except  openai.error.AuthenticationError as e:
            logging.error(f'Failed as {str(e)}')

    def post_dev(self, prompt: str) -> ChatGPTResponse:
        """
            Post a prompt/request to ChatGPT given the parameters defined in the constructor.
            The entire response is objectified
            :param prompt: Prompt or content of the request
            :return: ChatGPTResponse
        """
        import json
        import logging
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_gpt_request.model,
                messages=[{'role': self.chat_gpt_request.user, 'content': prompt}],
                temperature=self.chat_gpt_request.temperature,
                max_tokens=self.chat_gpt_request.max_tokens
            )
            return json.loads(response)
        except  openai.error.AuthenticationError as e:
            logging.error(f'Failed as {str(e)}')


if __name__ == '__main__':
    chat_gpt = ChatGPTClient.build('gpt-3.5-turbo', 'user', 0.0)
    context = 'the Moon'
    answer, num_tokens = chat_gpt.post(f'What is the color of {context}')
    print(f'Answer: {answer} with {num_tokens} tokens')
