# import re

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
obj = {"options": {"displayChrome": "yes", "downloadAudio": "yes", "downloadVideo": "no", "fileNames": ["Smoke Sessions"], "outputAudioFormat": "aac", "outputVideoFormat": "mp4", "promptCombine": "yes", "useVideoTitle": "no", "verbose": "yes"}, "outputDir": "tests", "urlsDir": "urls.txt"}
for key in obj:
	print(key)
	# print(val)
	# print(other)
