import json

#Utility script that pulls the itags from itagrw.txt and enumerates them for use of YTDL 

itags = {}
with open("itagrw.txt","r") as f:
	lines = f.read().splitlines()
	for i,line in enumerate(lines):
		itags[line.split(" ")[0]] = i
print(itags)
with open("itags.json","w") as f:
	data = json.dumps(itags,indent=4, sort_keys=True)
	f.write(data)
