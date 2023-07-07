__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import AnyStr, Sequence
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import BaseTool
from langchain.agents import AgentType
from llmbaseagent import LLMBaseAgent


class OpenAIFunctionAgent(object):

    """
        Constructor for the generic Agent that support Open AI functions
        :param _model Open AI model that supports functions
        :param _tools Sequence of tools supporting this agent
    """
    def __init__(self, _model: AnyStr, _tools: Sequence[BaseTool], cache_model: AnyStr):
        assert _model == "gpt-3.5-turbo-0613", f'Model {_model} does not support OpenAI functions'

        llm = ChatOpenAI(temperature=0, model=_model)
        self.open_ai_agent = initialize_agent(
            _tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )
        llm.llm_cache = LLMBaseAgent.set_cache(cache_model)

    def __call__(self, prompt):
        return self.open_ai_agent.run(prompt)
