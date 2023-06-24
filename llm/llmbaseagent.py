__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from langchain.agents import AgentType, AgentExecutor
from typing import AnyStr
from langchain.chat_models import ChatOpenAI


class LLMBaseAgent(object):
    """
        Generic LangChain agent to be used with ChatGPT
        :param chat_handle Handle or reference to the large language model
        :param agent LangChain agent executor
    """
    def __init__(self, chat_handle: ChatOpenAI, agent: AgentExecutor):
        self.chat_handle = chat_handle
        self.agent = agent

    def run(self, input_prompt_str: AnyStr) -> AnyStr:
        """
            :param input_prompt_str Input stream
            :return answer from ChatGPT
        """
        return self.agent.run(input_prompt_str)
