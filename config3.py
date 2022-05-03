import tkinter as tk

from tkinter import scrolledtext
from tkinter import ttk


if __name__ == '__main__':

    window = tk.Tk()
    window.title("My Program")
    tab_control = ttk.Notebook(window)

    tab1 = tk.Frame(tab_control)
    tab1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tab2 = tk.Frame(tab_control)
    tab2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tab_control.pack(fill=tk.BOTH, expand=True)
    tab_control.add(tab1, text='First')
    tab_control.add(tab2, text='Second')

    labe1frame_1 = tk.LabelFrame(tab1, text="Frame_1")
    labe1frame_1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    txtbox = scrolledtext.ScrolledText(labe1frame_1, width=40, height=10)
    txtbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    window.mainloop()