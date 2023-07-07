__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import AnyStr, Sequence
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain.agents import AgentType
from llmbaseagent import LLMBaseAgent


class OpenAIFunctionAgent(LLMBaseAgent):

    def __init__(self, chat_handle: ChatOpenAI, agent: AgentExecutor, cache_model: AnyStr):
        """
        Default constructor for OpenAI Function Agent
        @param chat_handle: Handle to LLM
        @param agent: Agent executor
        @param cache_model: Model for caching (SQL lite, in memory,...)
        """
        super(OpenAIFunctionAgent, self).__init__(chat_handle, agent, cache_model)

    @classmethod
    def build(cls, _model: AnyStr, _tools: Sequence[BaseTool], cache_model: AnyStr):
        """
        Detailed constructor with specific arguments
        @param _model: Open AI model that supports functions
        @param _tools: Sequence of tools supporting this agent
        @param cache_model: Cache model used for operations
        """
        assert _model in ["gpt-3.5-turbo-0613", "gpt-4.0"], f'Model {_model} does not support OpenAI functions'

        llm = ChatOpenAI(temperature=0, model=_model)
        open_ai_agent: AgentExecutor = initialize_agent(
            _tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True)
        return cls(llm, open_ai_agent, cache_model)

