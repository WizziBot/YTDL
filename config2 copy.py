
import sys
from tkinter import Tk, ttk, N, W, E, S, Frame, StringVar, BooleanVar
from tkinter.scrolledtext import ScrolledText

def rgbGet(rgb):
    return "#%02x%02x%02x" % rgb  

class PrintLogger(object):  # create file like object

	def __init__(self, textbox):  # pass reference to text widget
		self.textbox = textbox  # keep ref

	def write(self, text):
		self.textbox.configure(state="normal")  # make field editable
		self.textbox.insert("end", text)  # write text to textbox
		self.textbox.see("end")  # scroll to end
		self.textbox.configure(state="disabled")  # make field readonly

	def flush(self):  # needed for file like object
		pass

def rmFocus():
	pass

def styleConfig(style,font):
	# style.theme_use("default")
	style.configure("DG.TFrame", background='#303030')
	style.configure("DG.TCheckbutton", background='#303030',foreground="white",font=font)
	style.map('DG.TCheckbutton', background=[('active','#303030')])
	style.configure("DG.TButton",background='#303030',foreground='black',font=font)
	style.map('DG.TButton', background=[('active','#303030')])
	# print(style.layout("DG.TCheckbutton"))
	style.configure("DG.TLabel", background='#303030',foreground="white",font=font)
	style.layout("DG.TButton",[('Button.button',{'sticky': 'nswe', 'children': [('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})])
	style.layout("DG.TCheckbutton",[('Checkbutton.padding',{'sticky': 'nswe', 'children': [('Checkbutton.indicator',{'side': 'left', 'sticky': ''}), ('Checkbutton.label',{'sticky': 'nswe'})]})])

class MainGUI():

	def __init__(self):
		# Tk.__init__(self)
		self.root = Tk()
		self.root.title("YTDL CONFIGURATION")
		self.root.geometry("600x400")
		self.root.resizable(height=False,width=False)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		style = ttk.Style()
		self.font=("JetBrains Mono Medium", "10")
		styleConfig(style,self.font)
		self.mainwindow = ttk.Frame(self.root,style="RED.TFrame")
		self.mainwindow.grid(column=0, row=0, sticky=(N, W, E, S))
		self.mainwindow.grid_columnconfigure(1,weight=1)
		self.mainwindow.grid_rowconfigure(2,weight=1)
		self.mainFrameInit()
		self.cmdLogInit()
		self.mainLayoutInit()

		for child in self.mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

		self.cfg1_entry.focus()
		# self.root.bind("<Return>", self.calculate)

		self.log_widget = ScrolledText(self.bottomframe, height=4, width=120, font=self.font,background=rgbGet((35,45,60)),foreground="white")
		self.log_widget.grid(column=1,row=1,sticky=(N,S,E,W))

		self.redirect_logging()

	def mainFrameInit(self):
		self.mainframe = ttk.Frame(self.mainwindow, padding="10 25 10 15" ,style="DG.TFrame")
		self.mainframe.grid(column=1, row=1, sticky=(N, W, E))
		self.mainframe.grid_columnconfigure(0,weight=1)
		self.mainframe.grid_columnconfigure(4,weight=1)
		self.mainframe.grid_rowconfigure(0,weight=1)
		self.mainframe.grid_rowconfigure(4,weight=1)

	def cmdLogInit(self):
		self.bottomframe = ttk.Frame(self.mainwindow)
		self.bottomframe.grid(column=1, row=2, sticky=(N, W, E, S))
		self.bottomframe.grid_columnconfigure(1,weight=1)
		self.bottomframe.grid_rowconfigure(1,weight=1)

	# def calculate(self,*args):
	# 	try:
	# 		value = float(self.cfg1.get())
	# 		self.cfg2.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
	# 	except ValueError:
	# 		pass
	def saveConfig(self):
		print("Config Saved!")
	
	def vars(self,*args):
		print('var: {}'.format(self.cfg1.get()))
		print('data: {}'.format(args[0]))

	def varb(self,*args):
		print(f'Checked: {self.testbool.get()}')

	def reset_logging(self):
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__

	def redirect_logging(self):
		logger = PrintLogger(self.log_widget)
		sys.stdout = logger
		sys.stderr = logger

	def mainLayoutInit(self):
		self.Entries = []
		self.cfg1 = StringVar(value="something")
		# self.cfg1.trace('w', self.vars)
		self.cfg1_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.cfg1)
		self.cfg1_entry.grid(column=2, row=1, sticky=(W, E))

		self.cfg2 = StringVar()
		ttk.Entry(self.mainframe, textvariable=self.cfg2, width=30).grid(column=2, row=2, sticky=(W, E))

		ttk.Button(self.mainframe, text="SAVE", command=self.saveConfig, style="DG.TButton").grid(column=3, row=3, sticky=(N,E,S,W))

		ttk.Label(self.mainframe, text="CFG1", style="DG.TLabel").grid(column=1, row=1, sticky=W)
		self.testbool = BooleanVar()
		self.testbool.trace('w',self.varb)
		c1 = ttk.Checkbutton(self.mainframe, text = "OPTION",variable=self.testbool,style="DG.TCheckbutton")
		c1.grid(row = 3, column = 1, stick=E, columnspan = 1)

		ttk.Label(self.mainframe, text="CFG2", style="DG.TLabel").grid(column=1, row=2, sticky=W)


if __name__ == "__main__":
	app = MainGUI()
	app.root.mainloop()