
import subprocess
import os

def chEx(path):
	if not os.path.isdir(path):
		os.mkdir(path)

def toFormat(format,filePathIn,filePathOut,verbose):
	if format == "mp4" or format == "webm" or format == "mp3" or format == "m4a":
		cmd = f'ffmpeg -i {filePathIn} -acodec copy -vcodec copy {filePathOut}'
	elif format == "aac":
		cmd = f'ffmpeg -i {filePathIn} -acodec aac {filePathOut}'
	else:
		print("\nError: Unknown format.\n")
		return 1,0
	if verbose:
		retVal = subprocess.call(cmd, shell=True)
	else:
		retVal = subprocess.call(cmd, shell=True,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.STDOUT)
	if retVal == 0:
		os.remove(filePathIn)
	return retVal,filePathOut

def muxTracks(video,audio,outDir,verbose):
	outname = "-".join(video.split("-")[1:])
	cmd = f'ffmpeg -an -i temp/{video} -vn -i temp/{audio} -r 30 -acodec copy -vcodec copy {outDir}/{outname}'
	path = os.path.join(os.path.abspath("."), outDir)
	chEx(path)
	if verbose:
		retVal = subprocess.call(cmd, shell=True)
	else:
		retVal = subprocess.call(cmd, shell=True,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.STDOUT)
	if retVal == 0:
		os.remove(f'temp/{video}')
		os.remove(f'temp/{audio}')
	return retVal

def autoCombine(video,audio,outDir,config):
	if video.split(".")[-1] != config["outputVideoFormat"]:
		newVid = "".join(video.split(".")[:-1])+"."+config["outputVideoFormat"]
		if toFormat(config["outputVideoFormat"],"temp/"+video,"temp/"+newVid,(config["verbose"]=="yes"))[0] != 0:
			return 1,0
		video = newVid
	if audio.split(".")[-1] != config["outputVideoFormat"]:
		newAud = "".join(audio.split(".")[:-1])+"."+config["outputVideoFormat"]
		if toFormat(config["outputVideoFormat"],"temp/"+audio,"temp/"+newAud,(config["verbose"]=="yes"))[0] != 0:
			return 2,0
		audio = newAud

	if muxTracks(video,audio,outDir,(config["verbose"]=="yes")) != 0:
		return 3,0
	outname = "-".join(video.split("-")[1:])
	return 0,outDir+"/"+outname

if __name__ == "__main__":
	result = autoCombine("video-mfPCFQfOnLg.mp4","audio-mfPCFQfOnLg.webm")
	print(result)