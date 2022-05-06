# import re
import time
import asyncio
import threading
# text = "video-Interview with an Agile Coach in 2022 - Sprint2.mp4"
# # result = re.search("^video-(.*)",text).group(1)
# result = "-".join(text.split("-")[1:])
# print(result)

# from tkinter import *
# from tkinter import font
# root=Tk()
# fonts=font.families()
# for i in fonts:
#     print(i)

# with open("C:/Users/Rodriguez/OneDrive/Desktop/YTDL/test.txt","r") as f:
# 	print(f.read())
# obj = {"options": {"displayChrome": "yes", "downloadAudio": "yes", "downloadVideo": "no", "fileNames": ["Smoke Sessions"], "outputAudioFormat": "aac", "outputVideoFormat": "mp4", "promptCombine": "yes", "useVideoTitle": "no", "verbose": "yes"}, "outputDir": "tests", "urlsDir": "urls.txt"}
# for key in obj:
# 	print(key)
# 	# print(val)
# 	# print(other)

# def callbackFunc(var):
# 	print("Callback: "+var)

# def waitFunc(callb,loop):
# 	asyncio.set_event_loop(loop)
# 	getval = loop.run_until_complete()
# 	time.sleep(5)
# 	callb("something")


# def mainFunc():
# 	print("Here we go")
# 	loop = asyncio.new_event_loop()
# 	t = threading.Thread(target=waitFunc,args=(callbackFunc,loop))
# 	t.start()
# 	t.join()
# 	# waitFunc(callbackFunc)
# 	print("done")

# mainFunc()
# from tkinter import messagebox

# MsgBox = messagebox.askquestion ('YTDL','Combine Audio and Video tracks?',icon = 'info')
# print(MsgBox)

import os
path = os.path.join(os.path.abspath("."), "test2/") 
if not os.path.isdir(path):
	os.mkdir(path)
else:
	print("EXISTS")

