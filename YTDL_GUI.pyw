
import sys
from tkinter import Tk, ttk, N, W, E, S, StringVar, BooleanVar, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import time
import asyncio
from YTDL import mainloop
import threading

def rgbGet(rgb):
    return "#%02x%02x%02x" % rgb  

class PrintLogger(object):

	def __init__(self, textbox):  # pass reference to text widget
		self.textbox = textbox  # keep ref

	def write(self, text):
		self.textbox.configure(state="normal")  # make field editable
		self.textbox.insert("end", text)  # write text to textbox
		self.textbox.see("end")  # scroll to end
		self.textbox.configure(state="disabled")  # make field readonly

	def flush(self):
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
		self.mainRunning = False
		self.loadConfig()
		self.root = Tk()
		self.root.title("YTDL")
		self.root.geometry("600x600")
		self.root.resizable(height=False,width=False)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
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
		self.config["urlsDir"] = self.Entries[0][0].get().strip()
		self.config["outputDir"] = self.Entries[1][0].get().strip()
		self.config["options"]["outputVideoFormat"] = self.Entries[2][0].get().strip()
		self.config["options"]["outputAudioFormat"] = self.Entries[3][0].get().strip()

		for opt in self.Options:
			self.config["options"][opt[1]] = "yes" if opt[0].get() == True else "no"

		fileNames =  self.fileNames.get().strip()
		if fileNames == "":
			self.config["options"]["fileNames"] = []
		else:
			self.config["options"]["fileNames"] = fileNames.split(";")

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
			entryStr = StringVar(self.mainframe)
			entryW = ttk.Entry(self.mainframe, width=20, textvariable=entryStr)
			entryW.grid(column=2,row=i,sticky=(W,E))
			self.Entries.append((entryStr,entryW))
		self.Entries[0][0].set(self.config["urlsDir"])
		self.Entries[1][0].set(self.config["outputDir"])
		self.Entries[2][0].set(self.config["options"]["outputVideoFormat"])
		self.Entries[3][0].set(self.config["options"]["outputAudioFormat"])
	
	def setOptions(self):
		i=0
		j=0
		t=0
		length = len(self.OptionsMap[0]) + len(self.OptionsMap[1])
		while t < length:
			toggleOpt = BooleanVar(self.mainframe)
			ttk.Checkbutton(self.mainframe, text = self.OptionsMap[j][i][0],variable=toggleOpt,style="DG.TCheckbutton")\
				.grid(row = 2 + i, column = 3 + j, stick=W, columnspan = 1)
			toggleOpt.initialize(True if (self.config["options"][self.OptionsMap[j][i][1]] == "yes") else False)
			self.Options.append((toggleOpt,self.OptionsMap[j][i][1]))
			i = (i+1) % len(self.OptionsMap[0])
			j = (j+1) % len(self.OptionsMap)
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
		sys.stdin = self.logger

	def mkLabels(self,texts):
		for i,text in enumerate(texts,2):
			lbl = ttk.Label(self.mainframe, text=text, style="DG.TLabel").grid(column=1, row=i, sticky=W)
			self.Labels.append(lbl)

	async def waitUntil(arg):
		MsgBox = messagebox.askquestion('YTDL','Combine Audio and Video tracks?',icon = 'info')
		print("SELECTED: "+MsgBox+"\n")
		if MsgBox == "yes":
			return "y"
		else:
			return "n"
	
	def runmain(self):
		if self.mainRunning == False:
			self.mainRunning = True
			self.mainloop = asyncio.new_event_loop()
			if self.config["options"]["promptCombine"]:
				self.t = threading.Thread(target=mainloop,args=(self.waitUntil,self.mainloop))
			else:
				self.t = threading.Thread(target=mainloop,args=(0,self.mainloop))
			self.t.start()
		elif not self.t.is_alive():
			self.mainloop = asyncio.new_event_loop()
			if self.config["options"]["promptCombine"]:
				self.t = threading.Thread(target=mainloop,args=(self.waitUntil,self.mainloop))
			else:
				self.t = threading.Thread(target=mainloop,args=(0,self.mainloop))
			self.t.start()

	def on_closing(self):
		self.reset_logging()
		if hasattr(self,"t") and self.t.is_alive():
			print("CLOSED GUI")
			self.t.join()
			self.mainloop.close()
			self.mainRunning = False
		self.root.destroy()

	def mainLayoutInit(self):
		self.Entries = []
		self.Labels = []
		self.Options = []
		self.OptionsMap = [[("Display Chrome","displayChrome"),("Download Video","downloadVideo"),("Use YT Title","useYoutubeTitle")],\
			[("Verbose","verbose"),("Download Audio","downloadAudio"),("Prompt Combine","promptCombine")]]
		self.setEntries()
		self.mkLabels(["Urls file:","Output Folder:","Video Format:","Audio Format:"])
		self.setOptions()
		# Special widgets
		ttk.Label(self.mainframe, text = "YTDL CONFIGURATION", style="DG.TLabel")\
			.grid(column=2, row=1, columnspan=2)
		
		ttk.Label(self.mainframe, text = "File Names (separated by ;)", style="DG.TLabel")\
			.grid(column=3, row=5, columnspan=2)
		self.fileNames = StringVar(self.mainframe)
		ttk.Entry(self.mainframe, textvariable=self.fileNames)\
			.grid(column=3,row=6,columnspan=2,sticky=(W,E))
		self.fileNames.set(";".join(self.config["options"]["fileNames"]))

		ttk.Button(self.mainframe, text="SAVE", command=self.saveConfig, style="DG.TButton").grid(column=1, row=self.max_row, sticky=(N,E,S,W))
		ttk.Button(self.mainframe, text="RUN", command=self.runmain, style="DG.TButton").grid(column=2, row=self.max_row, sticky=(N,E,S,W))
		# ###


if __name__ == "__main__":
	app = MainGUI()
	app.root.mainloop()