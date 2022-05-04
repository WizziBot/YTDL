import json
import src.downloadFiles as dl
import src.networkRequest as nr
import src.combine as cmb
import re
import time
import asyncio

def validateURLS(urls):
	for url in urls:
		result = re.search("www\.youtube\.com/watch\?v=([^&]*)",url)
		if result:
			url = "https://www.youtube.com/watch?v="+result.group(1)
			# print("YIELDING:",url)
			yield url
		else:
			print(f'Error: Invalid URL ({url})')
			exit(1)

def verifyConfig(cfg):
	for key, value in cfg.items():
		if key == "urlsDir" and value == "":
			print("Error: Missing Url Directory.")
			exit(1)
		elif key == "outDir" and value == "":
			print("Error: Missing Output Directory.")
			exit(1)
		elif key == "options":
			for k,v in value.items():
				if ((k == "useYoutubeTitle" and v != "yes" and v != "no")
					or (k == "displayChrome" and v != "yes" and v != "no")
					or (k == "downloadVideo" and v != "yes" and v != "no")
					or (k == "downloadAudio" and v != "yes" and v != "no")
					or (k == "promptCombine" and v != "yes" and v != "no")
					or (k == "verbose" and v != "yes" and v != "no")):
					print("Error: Invalid entry for yes/no option '"+k+"'.")
					exit(1)
				elif (k == "outputVideoFormat" and v == "") or (k == "outputAudioFormat" and v == ""):
					print("Error: '"+k+"' must have a value.")
					exit(1)


def YTDL_Links(origUrl,config,i,itags):
	vidEn = True
	audEn = True
	if config["downloadVideo"] != "yes":
		vidEn = False
	if config["downloadAudio"] != "yes":
		audEn = False
	# Verify links
	title,links = nr.getLinks(origUrl,config)
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
		except IndexError:
			print("Error: Insuficient file names. (Check config.json)")
			exit(1)
	else:
		filePrefix = title
	return ((videolnk,"video-"+filePrefix+"."+videotyp),(audiolnk,"audio-"+filePrefix+"."+audiotyp)), (videoMins,videoSecs)

def mainloop(isGUI,smth,loop):
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main(isGUI,smth))


def main(isGUI,*args):
	with open("config.json","r") as f:
		raw = f.read()
		if raw == "":
			print("Error: Could not load config.json")
			exit(1)
		data = json.loads(raw)
		verifyConfig(data)
		urlsDir = data["urlsDir"]
		outDir = data["outputDir"]
		config = data["options"]
	with open("src/itags.json","r") as f:
		raw2 = f.read()
		if raw2 == "":
			print("Error: Could not load itags.json")
			exit(1)
		itags = json.loads(raw2)

	with open(urlsDir,"r") as f:
		urls = f.read().splitlines()
	if config["useYoutubeTitle"] != "yes":
		if config["fileNames"]:
			if len(config["fileNames"]) != len(urls):
				print("Error: Insufficient File Names")
				exit(1)
	for i,url in enumerate(validateURLS(urls)):
		print("[Processing] :",url)
		targets,videoTime = YTDL_Links(url,config,i,itags)
		if targets:
			print("[Retrieved Link Data]\n")
		else:
			print("Error: Could Not Process Links\n")
			continue
		# print(targets)
		comb = ""
		if config["downloadVideo"] == "yes" and config["downloadAudio"] == "yes" and config["promptCombine"] == "yes":
			if isGUI:
				print("\nCombine Audio and Video? [y/n]")
				# insert callback here (will contain rest of main)
				args[0]("something")
				comb = "y"
			else:
				comb = input("\nCombine Audio and Video? [y/n]: ")
				print()
		if config["useYoutubeTitle"] != "yes":
			print("[Downloading] ("+config["fileNames"][i]+") ("+str(videoTime[0])+"m "+str(videoTime[1])+"s"+")\n")
		else:
			print("[Downloading] ("+"-".join(targets[0][1].split("-")[1:])+") ("+str(videoTime[0])+"m "+str(videoTime[1])+"s"+")\n")
		if comb == "y" or config["promptCombine"] == "no":
			dl.downloadUrls(targets,"temp/")
			print("[Combining]")
			result = cmb.autoCombine(targets[0][1],targets[1][1],outDir,config)
			if result:
				print("[Combined Video and Audio tracks]\n")
			else:
				print("Error: Failed to combine Video and Audio tracks\n")
		else:
			if config["downloadVideo"] == "yes" and targets[0][1].split(".")[-1] != config["outputVideoFormat"]:
				dl.downloadUrls([targets[0]],"temp/")
				result = cmb.toFormat(config["outputVideoFormat"],"temp/"+targets[0][1],outDir+"/"+"".join(targets[0][1].split(".")[:-1])+"."+config["outputVideoFormat"],(config["verbose"]=="yes"))
				if result == 0:
					print(f'[Converted Video to {config["outputVideoFormat"]}]')
				else:
					print('Error: Failed to convert Video to '+config["outputVideoFormat"])
			elif config["downloadVideo"] == "yes":
				dl.downloadUrls([targets[0]],outDir+"/")
			if config["downloadAudio"] == "yes" and targets[1][1].split(".")[-1] != config["outputAudioFormat"]:
				dl.downloadUrls([targets[1]],"temp/")

				result = cmb.toFormat(config["outputAudioFormat"],"temp/"+targets[1][1],outDir+"/"+"".join(targets[1][1].split(".")[:-1])+"."+config["outputAudioFormat"],(config["verbose"]=="yes"))
				if result == 0:
					print(f'[Converted Audio to {config["outputAudioFormat"]}]')
				else:
					print('Error: Failed to convert Audio to '+config["outputAudioFormat"])
			elif config["downloadAudio"] == "yes":
				dl.downloadUrls([targets[1]],outDir+"/")
	print("\n----DONE----\n")

if __name__ == "__main__":
	main(False)