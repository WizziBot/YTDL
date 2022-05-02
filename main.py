import json
import src.downloadFiles as dl
import src.networkRequest as nr
import src.combine as cmb
import re
# import shutil

def YTDL_Links(origUrl,config,i):
	vidEn = True
	audEn = True
	if config["downloadVideo"].lower() != "yes":
		vidEn = False
	if config["downloadAudio"].lower() != "yes":
		audEn = False
	# Verify links
	title,links = nr.getLinks(origUrl,config)
	print("\n[Retrieved Link Data]\n")
	videolnk = ""
	videotyp = ""
	audiolnk = ""
	audiotyp = ""
	fileReq = [[False,0],[False,0]]
	for lnk in links:
		if vidEn and lnk[1] == "video" and (fileReq[0][0] == False or lnk[3] > fileReq[0][1]):
			videolnk = re.search("(.*)&range",lnk[0]).group(1)
			videotyp = lnk[2]
			fileReq[0][0] == True
			fileReq[0][1] = lnk[3]
		elif audEn and lnk[1] == "audio" and (fileReq[1][0] == False):
			audiolnk = re.search("(.*)&range",lnk[0]).group(1)
			audiotyp = lnk[2]
			fileReq[1][0] = True
	if (videolnk == "" and vidEn) or (audiolnk == "" and audEn):
		return False
	if config["useVideoTitle"].lower() != "yes":
		filePrefix = config["fileNames"][i].replace(" ","_")
	else:
		filePrefix = title
	return ((videolnk,"video-"+filePrefix+"."+videotyp),(audiolnk,"audio-"+filePrefix+"."+audiotyp))

		

if __name__ == "__main__":
	with open("config.json","r") as f:
		raw = f.read()
		data = json.loads(raw)
		urlDirs = data["urlDirs"] # loop over batches
		outDir = data["outputDir"]
		config = data["options"]
	for urlsDir in urlDirs:
		with open(urlsDir,"r") as f:
			urls = f.read().splitlines()
		if config["useVideoTitle"].lower() != "yes":
			if config["fileNames"]:
				if len(config["fileNames"]) != len(urls):
					print("Error: Insufficient File Names")
					exit(1)
		for i,url in enumerate(urls):
			print("[Processing] :",url)
			targets = YTDL_Links(url,config,i)
			if not targets:
				print("Error: Could Not Process Links")
				continue
			# print(targets)
			comb = ""
			if config["downloadVideo"].lower() == "yes" and config["downloadAudio"].lower() == "yes":
				comb = input("\nCombine Audio and Video?[y/n]: ")
			print()
			if config["useVideoTitle"].lower() != "yes":
				print("[Downloading] ("+config["fileNames"][i]+")\n")
			else:
				print("[Downloading] ("+re.search(".*-(.*)\.",targets[0][1]).group(1)+")\n")
			if comb == "y":
				dl.downloadUrls(targets,"temp/")
				print("[Combining]")
				result = cmb.autoCombine(targets[0][1],targets[1][1],outDir,config)
				if result:
					print("[Combined Video and Audio tracks]\n")
				else:
					print("Error: Failed to combine Video and Audio tracks\n")
			else:
				if config["downloadVideo"].lower() == "yes" and targets[0][1].split(".")[-1] != config["outputVideoFormat"]:
					dl.downloadUrls([targets[0]],"temp/")
					result = cmb.toFormat(config["outputVideoFormat"],"temp/"+targets[0][1],outDir+"/"+"".join(targets[0][1].split(".")[:-1])+"."+config["outputVideoFormat"],(config["verbose"].lower()=="yes"))
					if result == 0:
						print(f'[Converted Video to {config["outputVideoFormat"]}]')
					else:
						print('Error: Failed to convert Video to '+config["outputVideoFormat"])
				elif config["downloadVideo"].lower() == "yes":
					dl.downloadUrls([targets[0]],outDir+"/")
				if config["downloadAudio"].lower() == "yes" and targets[1][1].split(".")[-1] != config["outputAudioFormat"]:
					dl.downloadUrls([targets[1]],"temp/")

					result = cmb.toFormat(config["outputAudioFormat"],"temp/"+targets[1][1],outDir+"/"+"".join(targets[1][1].split(".")[:-1])+"."+config["outputAudioFormat"],(config["verbose"].lower()=="yes"))
					if result == 0:
						print(f'[Converted Audio to {config["outputAudioFormat"]}]')
					else:
						print('Error: Failed to convert Audio to '+config["outputAudioFormat"])
				elif config["downloadAudio"].lower() == "yes":
					dl.downloadUrls([targets[1]],outDir+"/")
	print("\n----DONE----\n")
