__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

import openai
from dataclasses import dataclass
from typing import TypeVar, AnyStr

Instancetype = TypeVar('Instancetype', bound='ChatGPTClient')


@dataclass
class ChatGPTRequest:
    """
        Data class for the generic request to ChatGPT API
        :param model Identifier of the model (i.e. gpt-3.5-turbo)
        :param user of the user {system|user|assistant}
        :param temperature hyper-parameters that adjusts the distribution (softmax) for the prediction of the next word/token
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
    # static variable for the API key and the default maximum number of tokens returned
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
    def build(cls, model: AnyStr, role: str, temperature: float) -> Instancetype:
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

    def post(self, prompt: AnyStr) -> (AnyStr, int):
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
        except openai.error.AuthenticationError as e:
            logging.error(f'Failed as {str(e)}')

    def post_dev(self, prompt: AnyStr) -> ChatGPTResponse:
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

    def post_streaming(self, prompt: AnyStr) -> (AnyStr, int):
        """
            Post a prompt/request to ChatGPT given the parameters defined in the constructor.
            The entire response is objectified
            :param prompt: Prompt or content of the request
            :return: ChatGPTResponse
        """
        import json
        import logging
        try:
            report = []
            result = ""
            last_response = None
            for response in openai.ChatCompletion.create(
                    model=self.chat_gpt_request.model,
                    messages=[{'role': self.chat_gpt_request.user, 'content': prompt}],
                    temperature=self.chat_gpt_request.temperature,
                    max_tokens=self.chat_gpt_request.max_tokens,
                    stream=True):
                last_response = response
                x = response
                report.append(response['choices'][0].delta.content)
                result = "".join(report).strip()
                print(result.replace("\n", ""))

            return result, last_response['usage'].total_tokens
        except openai.error.AuthenticationError as e:
            logging.error(f'Failed as {str(e)}')
            return "", -1


if __name__ == '__main__':
    chat_gpt = ChatGPTClient.build('gpt-3.5-turbo-0613', 'user', 0.0)
    context = 'the Moon'
    answer, num_tokens = chat_gpt.post(
        """Please compute the TF-IDF (Term frequency-Inverse Document frequency) score for words in the two documents 
        delimited by triple backticks,```this is a good time to walk```, ```but not a good time to run```"""
    )
    print(f'Answer: {answer} with {num_tokens} tokens')
