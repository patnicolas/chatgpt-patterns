__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import Any, AnyStr, Dict, Callable, List
from langchain.schema import AgentAction
from langchain.callbacks.base import BaseCallbackHandler


class LLMStartCallback(BaseCallbackHandler):
    def __init__(self, llm_start_func: Callable[[Dict[AnyStr, Any], List[AnyStr]], Any]):
        self.llm_start_func = llm_start_func

    def on_llm_start(self, serialized: Dict[AnyStr, Any], prompts: List[AnyStr], **kwargs: Any) -> Any:
        return self.llm_start_func(serialized, prompts)


class ChainStartCallback(BaseCallbackHandler):
    def __init__(self, chain_start_func: Callable[[Dict[AnyStr, Any], Dict[AnyStr, Any]], Any]):
        self.chain_start_func = chain_start_func

    def on_chain_start(self, serialized: Dict[AnyStr, Any], inputs:  Dict[AnyStr, Any], **kwargs: Any) -> Any:
        return self.chain_start_func(serialized, inputs)


class ToolStartCallback(BaseCallbackHandler):
    def __init__(self, tool_start_func: Callable[[Dict[AnyStr, Any], AnyStr], Any]):
        self.tool_start_func = tool_start_func

    def on_chain_start(self, serialized: Dict[AnyStr, Any], inputs:  AnyStr, **kwargs: Any) -> Any:
        return self.tool_start_func(serialized, inputs)


class AgentStartCallback(BaseCallbackHandler):
    def __init__(self, agent_start_func: Callable[[AgentAction, Any], Any]):
        self.agent_start_func = agent_start_func

    def on_chain_start(self, agent_action, **kwargs: Any) -> Any:
        return self.agent_start_func(agent_action, **kwargs)
