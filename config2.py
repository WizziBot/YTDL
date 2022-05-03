
import sys
from tkinter import Tk, ttk, N, W, E, S, Frame
from tkinter.scrolledtext import ScrolledText


style = ttk.Style()
style.configure("BSQ.TFrame", background="bisque")
style.configure("RED.TFrame", background="red")
style.configure("BLUE.TFrame", background="blue")
style.configure("RED.TLabel", background="red")
style.configure("BLUE.TLabel", background="blue")
style.configure("GREEN.TLabel", background="green")

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


class MainGUI(Tk):

	def __init__(self):
		# Tk.__init__(self)
		self.root = Tk()
		self.root.title("YTDL CONFIGURATION")
		self.root.geometry("600x400")
		mainwindow = ttk.Frame(self.root)
		mainwindow.grid(column=0, row=0, sticky=(N, W, E, S))
		mainwindow.grid_columnconfigure(1,weight=1)
		mainwindow.grid_rowconfigure(2,weight=1)
		mainframe = ttk.Frame(mainwindow, padding="10 25 10 15" ,style="BSQ.TFrame")
		mainframe.grid(column=1, row=1, sticky=(N, W, E))
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		mainframe.grid_columnconfigure(0,weight=1)
		mainframe.grid_columnconfigure(4,weight=1)
		mainframe.grid_rowconfigure(0,weight=1)
		mainframe.grid_rowconfigure(4,weight=1)
		bottomframe = ttk.Frame(mainwindow, padding="3 3 12 12" ,style="BLUE.TFrame")
		bottomframe.grid(column=1, row=2, sticky=(N, W, E, S))

		# self.root.pack(fill=BOTH,expand=True)
		# self.redirect_button = Button(self.root, text="Redirect console to widget", command=self.redirect_logging)
		# self.redirect_button.pack()
		# self.redirect_button = Button(self.root, text="Redirect console reset", command=self.reset_logging)
		# self.redirect_button.pack()
		# self.test_button = Button(self.root, text="Test Print", command=self.test_print)
		# self.test_button.pack()
		# self.log_widget = ScrolledText(self.root, height=4, width=120, font=("consolas", "8", "normal"))
		# self.log_widget.pack(fill=BOTH,expand=True)

	def reset_logging(self):
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__

	def test_print(self):
		print("Am i working?")

	def redirect_logging(self):
		logger = PrintLogger(self.log_widget)
		sys.stdout = logger
		sys.stderr = logger


if __name__ == "__main__":
	app = MainGUI()
	app.root.mainloop()