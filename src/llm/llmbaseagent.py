__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from langchain.agents import AgentExecutor
from langchain.cache import InMemoryCache, SQLiteCache
from typing import AnyStr
from langchain.chat_models import ChatOpenAI


class LLMBaseAgent(object):
    in_memory_cache = "in_memory_cache"
    sql_lite_cache = "sql_lite_cache"
    """
        Generic LangChain agent to be used with ChatGPT
        :param chat_handle Handle or reference to the large language model
        :param agent LangChain agent executor
    """
    def __init__(self, chat_handle: ChatOpenAI, agent: AgentExecutor, cache_model: AnyStr):
        self.chat_handle = chat_handle
        self.agent = agent
        self.chat_handle.llm_cache = LLMBaseAgent.set_cache(cache_model)

    @staticmethod
    def set_cache(cache_model: AnyStr):
        if cache_model == LLMBaseAgent.in_memory_cache:
            return InMemoryCache()
        elif cache_model == LLMBaseAgent.sql_lite_cache:
            return SQLiteCache(database_path=".langchain.db")
        else:
            return InMemoryCache()

    def run(self, input_prompt_str: AnyStr) -> AnyStr:
        """
            :param input_prompt_str Input stream
            :return answer from ChatGPT
        """
        return self.agent.run(input_prompt_str)
