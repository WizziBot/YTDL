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
	links = nr.getLinks(origUrl)
	# print("LINKSSS")
	# print(links)
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
	if config["useFileNames"].lower() == "yes":
		filePrefix = config["fileNames"][i]
	else:
		filePrefix = re.search("v=(.*)",origUrl).group(1)
	return ((videolnk,"video-"+filePrefix+"."+videotyp),(audiolnk,"audio-"+filePrefix+"."+audiotyp))

		

if __name__ == "__main__":
	with open("config.json","r") as f:
		raw = f.read()
		data = json.loads(raw)
		urlsDir = data["urls"]
		config = data["options"]
	with open(urlsDir,"r") as f:
		urls = f.readlines()
	if config["useFileNames"]:
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
		if config["useFileNames"].lower() == "yes":
			print("[Downloading] ("+config["fileNames"][i]+")\n")
		else:
			print("[Downloading] ("+url+")\n")
		dl.downloadUrls(targets)
		comb = ""
		if config["downloadVideo"].lower() == "yes" and config["downloadAudio"].lower() == "yes":
			comb = input("\nCombine Audio and Video?[y/n]: ")
		print()
		if comb == "y":
			result = cmb.autoCombine(targets[0][1],targets[1][1])
			if result:
				print("[Combined Video and Audio tracks]\n")
			else:
				print("Error: Failed to combine Video and Audio tracks\n")
	print("\n----DONE----\n")
