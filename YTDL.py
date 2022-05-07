import json
# import src.downloadFiles as dl
import src.downloadFilesL as dl
import src.networkRequest as nr
import src.combine as cmb
import re
import asyncio
from os import rename

def validateURLS(urls):
	for url in urls:
		result = re.search("www\.youtube\.com/watch\?v=([^&]*)",url)
		if result:
			url = "https://www.youtube.com/watch?v="+result.group(1)
			# print("YIELDING:",url)
			yield url
		else:
			print(f'Error: Invalid URL ({url})')
			print("Skipping URL...\n")
			continue

def verifyConfig(cfg):
	for key, value in cfg.items():
		if key == "urlsDir" and value == "":
			print("Error: Missing Url Directory.")
			return 1
		elif key == "outDir" and value == "":
			print("Error: Missing Output Directory.")
			return 1
		elif key == "options":
			for k,v in value.items():
				if ((k == "useYoutubeTitle" and v != "yes" and v != "no")
					or (k == "displayChrome" and v != "yes" and v != "no")
					or (k == "downloadVideo" and v != "yes" and v != "no")
					or (k == "downloadAudio" and v != "yes" and v != "no")
					or (k == "promptCombine" and v != "yes" and v != "no")
					or (k == "verbose" and v != "yes" and v != "no")):
					print("Error: Invalid entry for yes/no option '"+k+"'.")
					return 1
				elif (k == "outputVideoFormat" and v == "") or (k == "outputAudioFormat" and v == ""):
					print("Error: '"+k+"' must have a value.")
					return 1
	return 0

def cleanFileName(orig):
	modname = ""
	for x in orig:
		if x=="?" or x=="*" or x=="|" or x=="<" or x==">" or x=="\\" or x=="/" or x==":" or x=="\"":
			continue
		else:
			modname += x
	return modname

def YTDL_Links(origUrl,config,i,itags):
	vidEn = True
	audEn = True
	if config["downloadVideo"] != "yes":
		vidEn = False
	if config["downloadAudio"] != "yes":
		audEn = False
	# Verify links
	title,links = nr.getLinks(origUrl,config)
	origtitle = title
	print("\n[Processing Link Data]\n")
	videolnk = ""
	videotyp = ""
	audiolnk = ""
	audiotyp = ""
	fileReq = [[False,"219"],[False,"219"]]
	videoMins = 0
	videoSecs = 0
	for lnk in links:
		if vidEn and lnk[1] == "video" and (fileReq[0][0] == False or itags[lnk[3]] >= itags[fileReq[0][1]]):
			videolnk = re.search("(.*)&range",lnk[0]).group(1)
			videotyp = lnk[2]
			fileReq[0][0] == True
			fileReq[0][1] = lnk[3]
			if videoMins == 0:
				videoMins = round(float(lnk[4]) // 60)
				videoSecs = round(float(lnk[4]) % 60)
		elif audEn and lnk[1] == "audio" and (fileReq[1][0] == False or itags[lnk[3]] >= itags[fileReq[1][1]]):
			audiolnk = re.search("(.*)&range",lnk[0]).group(1)
			audiotyp = lnk[2]
			fileReq[1][0] = True
			if videoMins == 0:
				videoMins = round(float(lnk[4]) // 60)
				videoSecs = round(float(lnk[4]) % 60)
	if (videolnk == "" and vidEn) or (audiolnk == "" and audEn):
		return False, (0,0)
	filePrefix = ""
	if config["useYoutubeTitle"] != "yes":
		try:
			filePrefix = config["fileNames"][i].replace(" ","_")
			origtitle = cleanFileName(config["fileNames"][i])
		except IndexError:
			print("Error: Insuficient file names. (Check config.json)")
			print("Using Link Name...")
			filePrefix = re.search("www\.youtube\.com/watch\?v=([^&]*)",origUrl).group(1)
	else:
		if len(title) > 45:
			filePrefix = title[:45].replace(" ","_")
		else:
			filePrefix = title.replace(" ","_")
	return origtitle, ((videolnk,"video-"+filePrefix+"."+videotyp),(audiolnk,"audio-"+filePrefix+"."+audiotyp)), (videoMins,videoSecs)

def mainloop(logger,callback,loop):
	asyncio.set_event_loop(loop)
	status = loop.run_until_complete(main(logger,True,callback))
	if status == 0:
		print("STATUS: SUCCESS")
	else:
		print("STATUS: FAILURE")
	loop.close()


async def main(logger,isGUI,callback):
	with open("config.json","r") as f:
		raw = f.read()
		if raw == "":
			print("Error: Could not load config.json")
			return 1
		data = json.loads(raw)
		if verifyConfig(data) != 0:
			return 1
		urlsDir = data["urlsDir"]
		outDir = data["outputDir"]
		config = data["options"]
	with open("src/itags.json","r") as f:
		raw2 = f.read()
		if raw2 == "":
			print("Error: Could not load itags.json")
			return 1
		itags = json.loads(raw2)

	with open(urlsDir,"r") as f:
		urls = f.read().splitlines()
	if config["useYoutubeTitle"] != "yes":
		if config["fileNames"]:
			if len(config["fileNames"]) != len(urls):
				print("Error: Insufficient File Names")
				return 1
	for i,url in enumerate(validateURLS(urls)):
		print("[Processing] :",url)
		origTitle,targets,videoTime = YTDL_Links(url,config,i,itags)
		if targets:
			print("[Retrieved Link Data]\n")
		else:
			print("Error: Could Not Process Links\n")
			continue
		# print(targets)
		comb = ""
		if config["downloadVideo"] == "yes" and config["downloadAudio"] == "yes" and config["promptCombine"] == "yes":
			if isGUI:
				print("Combine Audio and Video? [y/n]")
				# insert callback here (will contain rest of main)
				response = await callback("-".join(targets[0][1].split("-")[1:]))
				comb = response
			else:
				comb = input("Combine Audio and Video? [y/n]: ")
				print()
		if config["useYoutubeTitle"] != "yes":
			print("[Downloading] ("+config["fileNames"][i]+") ("+str(videoTime[0])+"m "+str(videoTime[1])+"s"+")\n")
		else:
			print("[Downloading] ("+"-".join(targets[0][1].split("-")[1:])+") ("+str(videoTime[0])+"m "+str(videoTime[1])+"s"+")\n")
		if (comb == "y" or config["promptCombine"] == "no") and config["downloadVideo"] == "yes" and config["downloadAudio"] == "yes":
			await dl.downloadUrls(targets,"temp/")
			print("[Combining]")
			result,path = cmb.autoCombine(targets[0][1],targets[1][1],outDir,config)
			if result == 0:
				rename(path,outDir+"/"+origTitle+"."+config["outputVideoFormat"])
				print("[Combined Video and Audio tracks]\n")
			else:
				print("Error: Failed to combine Video and Audio tracks ("+str(result)+")\n")
		else:
			if config["downloadVideo"] == "yes" and targets[0][1].split(".")[-1] != config["outputVideoFormat"]:
				await dl.downloadUrls([targets[0]],"temp/")
				result, path = cmb.toFormat(config["outputVideoFormat"],"temp/"+targets[0][1],outDir+"/"+"".join(targets[0][1].split(".")[:-1])+"."+config["outputVideoFormat"],(config["verbose"]=="yes"))
				if result == 0:
					rename(path,outDir+"/"+origTitle+"."+config["outputVideoFormat"])
					print(f'[Converted Video to {config["outputVideoFormat"]}]')
				else:
					print('Error: Failed to convert Video to '+config["outputVideoFormat"])
			elif config["downloadVideo"] == "yes":
				await dl.downloadUrls([targets[0]],outDir+"/")
				rename(outDir+"/"+targets[0][1],outDir+"/"+"."+origTitle+config["outputVideoFormat"])
			if config["downloadAudio"] == "yes" and targets[1][1].split(".")[-1] != config["outputAudioFormat"]:
				await dl.downloadUrls([targets[1]],"temp/")

				result, path = cmb.toFormat(config["outputAudioFormat"],"temp/"+targets[1][1],outDir+"/"+"".join(targets[1][1].split(".")[:-1])+"."+config["outputAudioFormat"],(config["verbose"]=="yes"))
				if result == 0:
					rename(path,outDir+"/"+origTitle+"."+config["outputAudioFormat"])
					print(f'[Converted Audio to {config["outputAudioFormat"]}]')
				else:
					print('Error: Failed to convert Audio to '+config["outputAudioFormat"])
			elif config["downloadAudio"] == "yes":
				await dl.downloadUrls([targets[1]],outDir+"/")
				rename(outDir+"/"+targets[1][1],outDir+"/"+origTitle+"."+config["outputAudioFormat"])
	print("\n----DONE----\n")
	return 0

if __name__ == "__main__":
	import sys
	asyncio.run(main(False,False,0))