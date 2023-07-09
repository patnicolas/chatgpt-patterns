# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from typing import AnyStr


def simple_query_contractor_test(prompt: AnyStr):
    from src.llm.openaifunctionagent import OpenAIFunctionAgent
    from test.domain.simplequeryentities import SimpleQueryEntities

    tools = [SimpleQueryEntities()]
    open_ai_function_agent = OpenAIFunctionAgent("gpt-3.5-turbo-0613", tools)
    answer = open_ai_function_agent(prompt)
    print(answer)


def query_contractor_test(prompt: AnyStr):
    from src.domain.simplequerycontractors import SimpleQueryContractors
    from src.domain import HTMLTable
    from langchain.chat_models import ChatOpenAI
    from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

    tools = [SimpleQueryContractors(), HTMLTable()]
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    planner = load_chat_planner(llm)
    executor = load_agent_executor(llm, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
    answer = agent.run(prompt)
    # open_ai_function_agent = OpenAIFunctionAgent("gpt-3.5-turbo-0613", tools)
    # answer = open_ai_function_agent(prompt)
    print(answer)


def list_contractor_test(prompt: AnyStr):
    from src.llm.openaifunctionagent import OpenAIFunctionAgent
    from src.domain.listcontractors import ListContractors

    tools = [ListContractors()]
    open_ai_function_agent = OpenAIFunctionAgent("gpt-3.5-turbo-0613", tools)
    answer = open_ai_function_agent(prompt)
    print(answer)






if __name__ == '__main__':
    prompt1 = "List names, specialty and availability of all the contractors which location = San Jose. Display the {list} as HTML table"
    query_contractor_test(prompt1)

    """
    x = np.array([0.5, 1.9])
    y = x + 1.0
    print(y)

    from tkinter import *
    from tkinter import ttk
    from tkinter.messagebox import askyesno

    # creating root
    root = Tk()
    root.geometry('500x300')
    root.title('My pane')

    input_text = StringVar(root, "this is an entry")

    # This class is used to add styling
    # to any widget which are available
    style = ttk.Style()
    style.configure('TEntry', foreground='black')

    entry1 = ttk.Entry(root, textvariable=input_text, justify=CENTER,
                       font=('courier', 15, 'bold'))
    entry1.focus_force()
    entry1.pack(side=TOP, ipadx=30, ipady=10)

    save = ttk.Button(root, text='Save', command=lambda: askyesno(
        'Confirm', 'Do you want to save?'))
    save.pack(side=TOP, pady=10)
    root.mainloop()
    """

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
