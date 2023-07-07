__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from langchain.tools import BaseTool, StructuredTool
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType, AgentExecutor
from langchain.tools.python.tool import PythonREPLTool
from langchain.chat_models import ChatOpenAI
from typing import Optional, List, TypeVar, AnyStr
from src.llm.llmbaseagent import LLMBaseAgent

Instancetype = TypeVar('Instancetype', bound='ChatGPTToolAgent')


class LLMToolAgent(LLMBaseAgent):
    def __init__(self, chat_handle: ChatOpenAI, agent: AgentExecutor, _tools_list: List[AnyStr], cache_model: AnyStr):
        super(LLMToolAgent, self).__init__(chat_handle, agent, cache_model)
        self.tools_list = _tools_list

    @classmethod
    def build(cls,
              _tools_list: List[AnyStr],
              agent_type: Optional[AgentType],
              _handle_parsing_errors: bool) -> Instancetype:
        chat_handle = ChatOpenAI(temperature=0)
        agent = initialize_agent(
            load_tools(_tools_list, llm=chat_handle),
            chat_handle,
            agent=agent_type,
            handle_parsing_errors=_handle_parsing_errors,
            verbose=True
        )
        return cls(chat_handle, agent, _tools_list)

    def append(self, tool_name: AnyStr) -> List[AnyStr]:
        self.tools_list.append(tool_name)
        self.agent = initialize_agent(
            load_tools(self.tools_list, llm=self.chat_handle),
            self.chat_handle,
            handle_parsing_errors=self.agent.handle_parsing_errors,
            verbose=True
        )
        return self.tools_list

    def append_tool(self,  new_tool: BaseTool) -> List[AnyStr]:
        """
            :param new_tool New tool to be added to this agent
            :return list of current
        """
        self.tools_list.append(new_tool.name)
        tool_list = []
        for tool in self.agent.tools:
            tool_list.append(tool)
        tool_list.append(new_tool)
        self.agent = initialize_agent(
            tool_list,
            self.chat_handle,
            handle_parsing_errors=self.agent.handle_parsing_errors,
            verbose=True
        )
        return self.tools_list




if __name__ == '__main__':

    tool_names = ['llm-math']
    llm_tool_agent = LLMToolAgent.build(tool_names, AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, True)

    list_tool_names = llm_tool_agent.append_tool(PythonREPLTool())
    print(str(list_tool_names))

    from src.domain import load_contractors
    json_tool = StructuredTool.from_function(
            func=load_contractors,
            name="load_contractors",
            description="Load the list of contractors in JSON format"
        )
    list_tool_names = llm_tool_agent.append_tool(json_tool)
    print(str(list_tool_names))

    llm_tool_agent.run("List names of all the contractors")
