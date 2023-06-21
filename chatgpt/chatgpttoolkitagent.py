__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from chatgpt.chatgptagent import ChatGPTAgent
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.tools.json.tool import JsonSpec
from typing import AnyStr, TypeVar, Any

Instancetype = TypeVar('Instancetype', bound='ChatGPTToolkitAgent')


class ChatGPTToolkitAgent(ChatGPTAgent):
    """
        Wrapper for agent which rely on LangChain tool kits suc as Pandas dataframe
            file system, SQL database, Spark query, Json, CSV file loading..

        :param chat_handle Handle or reference to the large language model
        :param agent LangChain agent executor
    """
    def __init__(self, chat_handle: ChatOpenAI, agent: AgentExecutor):
        super(ChatGPTToolkitAgent, self).__init__(chat_handle, agent)

    @classmethod
    def build_from_toolkit(cls,  chat_handle: ChatOpenAI, agent_name: AnyStr, argument: Any) -> Instancetype:
        """
            Constructor to instantiate the agent from toolkits
                - Pandas dataframe
                - Spark SQL
                - SQL database
                - Json file loading
                - CSV file loading
                - ...
            :param chat_handle Handle or reference to the large language model
            :param agent_name name of agent
            :param argument Parameter for agent or toolkit (pd.Dataframe for Pandas, Spark Dataframe
        """
        if agent_name == "pandas_dataframe":
            from langchain.agents import create_pandas_dataframe_agent

            if argument.__class__.__name != 'pd.Dataframe':
                raise NotImplementedError(f'Agent {agent_name} should have argument of type pd.Dataframe')
            pandas_agent = create_pandas_dataframe_agent(llm=chat_handle, df=argument, verbose=True)
            return cls(chat_handle, pandas_agent)

        elif agent_name == "sql_database":
            from langchain.agents.agent_toolkits import SQLDatabaseToolkit
            from langchain.agents import create_sql_agent

            sql_toolkit = SQLDatabaseToolkit(db=argument, llm=chat_handle)
            sql_agent = create_sql_agent(llm=chat_handle, toolkit=sql_toolkit, verbose=True)
            return cls(chat_handle, sql_agent)

        elif agent_name == "json":
            import json
            from langchain.agents.agent_toolkits import JsonToolkit
            from langchain.agents import create_json_agent

            with open(argument) as f:
                data = json.load(f)
                json_spec = JsonSpec(dict_=data, max_value_length=4096)
                json_toolkit = JsonToolkit(spec=json_spec)
                json_agent = create_json_agent(llm=chat_handle, toolkit=json_toolkit, verbose=True)
                return cls(chat_handle, json_agent)

        elif agent_name == "csv":
            from langchain.agents import create_csv_agent

            csv_agent = create_csv_agent(chat_handle, argument, verbose=True)
            return cls(chat_handle, csv_agent)

        elif agent_name == "spark_sql":
            from langchain.utilities.spark_sql import SparkSQL
            from langchain.agents import create_spark_sql_agent
            from langchain.agents.agent_toolkits import SparkSQLToolkit

            spark_sql = SparkSQL(schema=argument)
            spark_sql_agent = create_spark_sql_agent(
                llm=chat_handle,
                toolkit=SparkSQLToolkit(db=spark_sql, llm=chat_handle),
                verbose=True)
            return cls(chat_handle, spark_sql_agent)

        else:
            raise NotImplementedError(f'Agent {agent_name} is not supported')


