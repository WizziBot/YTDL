
import subprocess
import os

def toFormat(format,filePathIn,filePathOut,verbose):
	if format == "mp4" or format == "webm" or format == "mp3" or format == "m4a":
		cmd = f'ffmpeg -i {filePathIn} -acodec copy -vcodec copy {filePathOut}'
	elif format == "aac":
		cmd = f'ffmpeg -i {filePathIn} -acodec aac {filePathOut}'
	else:
		return
	if verbose:
		retVal = subprocess.call(cmd, shell=True)
	else:
		retVal = subprocess.call(cmd, shell=True,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.STDOUT)
	if retVal == 0:
		os.remove(filePathIn)
	return retVal

def muxTracks(video,audio,outDir,verbose):
	outname = "-".join(video.split("-")[1:])
	cmd = f'ffmpeg -an -i temp/{video} -vn -i temp/{audio} -r 30 -acodec copy -vcodec copy {outDir}/{outname}'
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
		if toFormat(config["outputVideoFormat"],"temp/"+video,"temp/"+newVid,(config["verbose"]=="yes")) != 0:
			return False
		video = newVid
	if audio.split(".")[-1] != config["outputVideoFormat"]:
		newAud = "".join(audio.split(".")[:-1])+"."+config["outputVideoFormat"]
		if toFormat(config["outputVideoFormat"],"temp/"+audio,"temp/"+newAud,(config["verbose"]=="yes")) != 0:
			return False
		audio = newAud

	if muxTracks(video,audio,outDir,(config["verbose"]=="yes")) != 0:
		try:
			os.remove(f'temp/{video}')
			os.remove(f'temp/{audio}')
		except Exception as e:
			pass
		finally:
			return False
	return True

if __name__ == "__main__":
	result = autoCombine("video-mfPCFQfOnLg.mp4","audio-mfPCFQfOnLg.webm")
	print(result)