# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

from typing import AnyStr, Dict, List, Any

def load_contractors(filename: AnyStr) -> List[Dict[AnyStr, Any]]:
    from domain.contractors import Contractors
    return Contractors.load(filename)

class CustomToolsList(object):
    @staticmethod
    def run(prompt: AnyStr) -> AnyStr:
        from domain.contractor import load_contractors
        from chatgpt.chatgpttoolagent import ChatGPTToolAgent
        from langchain.tools import StructuredTool
        from langchain.agents import AgentType
        from langchain.tools.python.tool import PythonREPLTool

        tool_names = ['llm-math']
        chat_gpt_tool_agent = ChatGPTToolAgent.build(
            tool_names,
            AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            True)
        chat_gpt_tool_agent.append_tool(PythonREPLTool())
        json_tool = StructuredTool.from_function(
            func=load_contractors,
            name="load_contractors",
            description="Load the list of contractors given the file in folder data. load_contractors in module domain.contractor"
        )
        chat_gpt_tool_agent.append_tool(json_tool)
        return chat_gpt_tool_agent.run(prompt)


if __name__ == '__main__':
    CustomToolsList.run("List names of all the contractors specialized in plumbing, located in San Jose")

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
