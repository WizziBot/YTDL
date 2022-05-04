
from distutils.command.config import config
import sys
from tkinter import Tk, ttk, N, W, E, S, Frame, StringVar, BooleanVar
from tkinter.scrolledtext import ScrolledText
import json

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
		self.loadConfig()
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
		self.max_row = 6
		self.mainFrameInit()
		self.cmdLogInit()
		self.mainLayoutInit()

		for child in self.mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

		# self.cfg1_entry.focus()

	def mainFrameInit(self):
		self.mainframe = ttk.Frame(self.mainwindow, padding="10 25 10 15" ,style="DG.TFrame")
		self.mainframe.grid(column=1, row=1, sticky=(N, W, E))
		self.mainframe.grid_columnconfigure(0,weight=1)
		self.mainframe.grid_columnconfigure(5,weight=1)
		self.mainframe.grid_rowconfigure(0,weight=1)
		self.mainframe.grid_rowconfigure(self.max_row+1,weight=1)

	def cmdLogInit(self):
		self.bottomframe = ttk.Frame(self.mainwindow)
		self.bottomframe.grid(column=1, row=2, sticky=(N, W, E, S))
		self.bottomframe.grid_columnconfigure(1,weight=1)
		self.bottomframe.grid_rowconfigure(1,weight=1)
		self.log_widget = ScrolledText(self.bottomframe, height=4, width=120, font=self.font,background=rgbGet((35,45,60)),foreground="white")
		self.log_widget.grid(column=1,row=1,sticky=(N,S,E,W))
		self.redirect_logging()

	def saveConfig(self):
		self.config["urlsDir"] = self.Entries[0][0].get()
		self.config["outputDir"] = self.Entries[1][0].get()
		self.config["options"]["outputVideoFormat"] = self.Entries[2][0].get()
		self.config["options"]["outputAudioFormat"] = self.Entries[3][0].get()
		with open("config.json","w") as f:
			f.write(json.dumps(self.config,indent=4, sort_keys=True))
		print("Config Saved!")
	
	def loadConfig(self):
		with open("config.json","r") as f:
			raw = f.read()
			if raw == "":
				print("Error: Could not load config.json")
				exit(1)
			self.config = json.loads(raw)
	
	def setEntries(self):
		for i in range(2,self.max_row):
			entryStr = StringVar()
			entryW = ttk.Entry(self.mainframe, width=20, textvariable=entryStr)
			entryW.grid(column=2,row=i,sticky=(W,E))
			self.Entries.append((entryStr,entryW))
		self.Entries[0][0].set(self.config["urlsDir"])
		self.Entries[1][0].set(self.config["outputDir"])
		self.Entries[2][0].set(self.config["options"]["outputVideoFormat"])
		self.Entries[3][0].set(self.config["options"]["outputAudioFormat"])
	
	def setOptions(self,labels):
		i=0
		j=0
		t=0
		length = len(labels[0]) + len(labels[1])
		while t < length:
			toggleOpt = BooleanVar()
			optionW = ttk.Checkbutton(self.mainframe, text = labels[j][i],variable=toggleOpt,style="DG.TCheckbutton")\
				.grid(row = 2 + i, column = 3 + j, stick=W, columnspan = 1)
			self.Options.append((toggleOpt,optionW))
			i = (i+1) % len(labels[0])
			j = (j+1) % len(labels)
			t += 1


	def vars(self,*args):
		print('var: {}'.format(self.cfg1.get()))
		print('data: {}'.format(args[0]))

	def varb(self,*args):
		print(f'Checked: {self.testbool.get()}')

	def reset_logging(self):
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__

	def redirect_logging(self):
		self.logger = PrintLogger(self.log_widget)
		sys.stdout = self.logger
		sys.stderr = self.logger

	def mkLabels(self,texts):
		for i,text in enumerate(texts,2):
			lbl = ttk.Label(self.mainframe, text=text, style="DG.TLabel").grid(column=1, row=i, sticky=W)
			self.Labels.append(lbl)

	def mainLayoutInit(self):
		self.Entries = []
		self.Labels = []
		self.Options = []
		self.setEntries()
		self.mkLabels(["Urls file:","Output Folder:","Video Format:","Audio Format:"])
		self.setOptions([["Display Chrome","Download Video","Use YT Title"],["Verbose","Download Audio","Prompt Combine"]])
		# Special widgets
		ttk.Label(self.mainframe, text = "YTDL CONFIGURATION", style="DG.TLabel")\
			.grid(column=2, row=1, columnspan=2)

		ttk.Button(self.mainframe, text="SAVE", command=self.saveConfig, style="DG.TButton").grid(column=3, row=self.max_row, sticky=(N,E,S,W))
		# ###
		# self.testbool = BooleanVar()
		# self.testbool.trace('w',self.varb)
		# c1 = ttk.Checkbutton(self.mainframe, text = "OPTION",variable=self.testbool,style="DG.TCheckbutton")
		# c1.grid(row = self.max_row, column = 1, stick=E, columnspan = 1)


if __name__ == "__main__":
	app = MainGUI()
	app.root.mainloop()