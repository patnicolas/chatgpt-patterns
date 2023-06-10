__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from collections.abc import Callable
from chatgpt import load_api_key
import openai


def get_template(**kwargs: dict[str, any]) -> str:
    style = kwargs['language']
    text = kwargs['text']
    return """Translate the text that is delimited by triple backticks into a language {language}. text ```{text}```"""


class ChatGPTChain(object):
    openai.api_key = load_api_key()

    def __init__(self, temp: float, template: Callable[dict[str, any], str]):
        self.template = template
        self.chat = ChatOpenAI(temperature=temp)

    def get_arguments(self, **kwargs: dict[str, any]) -> list[str]:
        prompt_template = self.__get_prompt(**kwargs)
        return prompt_template.messages[0].input_variables

    def __call__(self, **kwargs: dict[str, any]) -> str:
        import logging
        try:
            prompt_template = self.__get_prompt(**kwargs)
            new_messages = prompt_template.format_messages(**kwargs)

            response = self.chat(new_messages)
            return response.content
        except openai.error.AuthenticationError as e:
            logging.error(str(e))
            return ""

    
    def __get_prompt(self, **kwargs):
        template_str = self.template(**kwargs)
        return ChatPromptTemplate.from_template(template_str)


if __name__ == '__main__':
    chat_gpt_chain = ChatGPTChain(0.2, get_template)
    response = chat_gpt_chain(**{'language':'french', 'text':'this is a good time to walk'})
    print(response)

