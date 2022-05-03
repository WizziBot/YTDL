import json
import src.downloadFiles as dl
import src.networkRequest as nr
import src.combine as cmb
import re

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
	if config["useVideoTitle"] != "yes":
		filePrefix = config["fileNames"][i].replace(" ","_")
	else:
		filePrefix = title
	return ((videolnk,"video-"+filePrefix+"."+videotyp),(audiolnk,"audio-"+filePrefix+"."+audiotyp)), (videoMins,videoSecs)

if __name__ == "__main__":
	with open("config.json","r") as f:
		raw = f.read()
		data = json.loads(raw)
		urlsDir = data["urlsDir"]
		outDir = data["outputDir"]
		config = data["options"]
	with open("src/itags.json","r") as f:
		raw2 = f.read()
		if raw2 == "":
			print("Error: Could not load Itags")
			exit(1)
		itags = json.loads(raw2)

	with open(urlsDir,"r") as f:
		urls = f.read().splitlines()
	if config["useVideoTitle"] != "yes":
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
			comb = input("\nCombine Audio and Video?[y/n]: ")
		print()
		if config["useVideoTitle"] != "yes":
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
