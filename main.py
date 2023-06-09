# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np


if __name__ == '__main__':
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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
