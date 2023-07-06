__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import AnyStr, Sequence
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import BaseTool
from langchain.agents import AgentType


class OpenAIFunctionAgent(object):
    """
        Constructor for the generic Agent that support Open AI functions
        :param _model Open AI model that supports functions
        :param _tools Sequence of tools supporting this agent
    """
    def __init__(self, _model: AnyStr, _tools: Sequence[BaseTool]):
        assert _model == "gpt-3.5-turbo-0613", f'Model {_model} does not support OpenAI functions'

        llm = ChatOpenAI(temperature=0, model=_model)
        self.open_ai_agent = initialize_agent(
            _tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

    def __call__(self, prompt):
        return self.open_ai_agent.run(prompt)
