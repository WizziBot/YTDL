from doctest import testfile
from tkinter import *
from tkinter import ttk

#indent=4, sort_keys=True (JSON)

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

root = Tk()
root.title("Feet to Meters")
root.geometry("600x400")
root.resizable(height=False,width=False)

style = ttk.Style()
style.configure("BSQ.TFrame", background="bisque")
style.configure("RED.TFrame", background="red")
style.configure("BLUE.TFrame", background="blue")
style.configure("RED.TLabel", background="red")
style.configure("BLUE.TLabel", background="blue")
style.configure("GREEN.TLabel", background="green")
mainwindow = ttk.Frame(root)
mainwindow.grid(column=0, row=0, sticky=(N, W, E, S))
mainwindow.grid_columnconfigure(1,weight=1)
mainwindow.grid_rowconfigure(2,weight=1)
mainframe = ttk.Frame(mainwindow, padding="10 25 10 15" ,style="BSQ.TFrame")
mainframe.grid(column=1, row=1, sticky=(N, W, E))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.grid_columnconfigure(0,weight=1)
mainframe.grid_columnconfigure(4,weight=1)
mainframe.grid_rowconfigure(0,weight=1)
mainframe.grid_rowconfigure(4,weight=1)
bottomframe = ttk.Frame(mainwindow, padding="3 3 12 12" ,style="BLUE.TFrame")
bottomframe.grid(column=1, row=2, sticky=(N, W, E, S))


# def validate(newtext):
#     print('validate: {}'.format(newtext))
#     return True
# vcmd = mainframe.register(validate)

# def key(event):
#     print('key: {}'.format(event.char))

def vars(*args):
	print('var: {} (args {})'.format(feet.get(), args))

def varb(*args):
	print(f'Checked: {testbool.get()}')

feet = StringVar(value="44")
feet.trace('w', vars)
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet) #,validate="key",validatecommand=(vcmd,'%P'))
feet_entry.grid(column=2, row=1, sticky=(W, E))
# feet_entry.bind('<Key>',key)
# feet_entry.columnconfigure()

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate,).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet", style="RED.TLabel").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="is equivalent to", style="BLUE.TLabel").grid(column=1, row=2, sticky=E)
testbool = BooleanVar()
c1 = ttk.Checkbutton(mainframe, text = "OPTION",variable=testbool)
testbool.trace('w',varb)
c1.grid(row = 2, column = 1, stick=E, columnspan = 1)

ttk.Label(mainframe, text="meters", style="GREEN.TLabel").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)


calculate()
root.mainloop()