# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from typing import AnyStr


def execute_openai_function(prompt: AnyStr) -> AnyStr:
    from src.llm_langchain.openaifunctionagent import OpenAIFunctionAgent
    from test.domain.simplequeryentities import SimpleQueryEntities

    tools = [SimpleQueryEntities()]
    open_ai_function_agent = OpenAIFunctionAgent.build("gpt-3.5-turbo-0613", tools)
    return open_ai_function_agent(prompt)


if __name__ == '__main__':
    from llm_openai.chatgptclient import ChatGPTClient
    chat_gpt = ChatGPTClient.build('gpt-3.5-turbo-0613', 'user', 0.0)
    input_prompt = """Please compute the TF-IDF (Term frequency-Inverse Document frequency) score for words in the two documents 
        delimited by triple backticks,```this is a good time to walk```, ```but not a good time to run```"""

    answer, num_tokens = chat_gpt.post(input_prompt)
    print(f'Answer: {answer} with {num_tokens} tokens')

    answer = execute_openai_function(input_prompt)
    print(f'Answer 2: {answer}')



