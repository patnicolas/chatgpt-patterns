__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

import openai
from chatgpt.chatgptclient import ChatGPTRequest
import tkinter as tk
from tkinter import ttk, StringVar


class ChatGPTBot(object):
    import constants
    # static variable for the API key and the default maximum number of tokens returned
    openai.api_key = constants.openai_api_key
    default_max_tokens = 128

    def __init__(self, context: str, chatGPTRequest: ChatGPTRequest):
        self.context = [{'role':'system', 'content':context}]
        self.chatGPTRequest = chatGPTRequest
        self.window = tk.Tk()
        self.window.title("Chat Bot")
        self.window.geometry("340x220")
        frm = ttk.Frame(self.window, padding = 12)
        frm.grid()
        frm.pack()
        ttk.Label(frm, text='My entry').grid(column = 0, row = 0)
        entry_var = StringVar(self.window, name = 'entry_var')
        entry_var.set('hello var')
        ttk_entry = ttk.Entry(frm, textvariable = entry_var)
        ttk_entry.pack()
        # Create an entry widget for user input
        self.button = ttk.Button(frm, text='Send', command=self.window.destroy)
        self.button.grid(column=1, row=0)
        self.button.pack()
        self.window.mainloop()

    def get_current_context(self) -> list:
        return self.context

    def post(self, prompt: str) -> str:
        """
        Post a prompt/request to ChatGPT given the parameters defined in the constructor.
        It only returns the content of the message
        :param prompt: Prompt or content of the request
        :return: First choice message content
        """
        import logging
        try:
            self.__update('user', prompt)
            response = openai.ChatCompletion.create(
                model=self.chatGPTRequest.model,
                messages=self.context,
                temperature=self.chatGPTRequest.temperature,
                max_tokens=self.chatGPTRequest.max_tokens
            )
            response_content = response['choices'][0].message.content
            self.__update('assistant', response_content)
            return response_content
        except  openai.error.AuthenticationError as e:
            logging.error(f'Failed as {str(e)}')

    def display(self):
        prompt = self.entry
        print(prompt)

    def __update(self, role: str, prompt: str):
        self.context.append({'role': role, 'content': prompt})


if __name__ == '__main__':
    """
    model = 'gpt-3.5-turbo'
    role = 'system'
    temperature = 0
    chat_gpt_request = ChatGPTRequest(model, role, temperature, 128, 1, 1, 0, 0)
    chat_gpt_bot = ChatGPTBot("this is the first context", chat_gpt_request)
    """

    from tkinter import *
    from tkinter import ttk
    from tkinter.messagebox import askyesno

    # creating root
    root = Tk()
    root.geometry('200x100')

    input_text = StringVar()

    # This class is used to add styling
    # to any widget which are available
    style = ttk.Style()
    style.configure('TEntry', foreground='green')

    entry1 = ttk.Entry(root, textvariable=input_text, justify=CENTER,
                       font=('courier', 15, 'bold'))
    entry1.focus_force()
    entry1.pack(side=TOP, ipadx=30, ipady=10)

    save = ttk.Button(root, text='Save', command=lambda: askyesno(
        'Confirm', 'Do you want to save?'))
    save.pack(side=TOP, pady=10)
