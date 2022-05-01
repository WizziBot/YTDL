
import subprocess

def toMP4(fileName):
	cmd = f'ffmpeg -i temp/{fileName} -c copy temp/{fileName.split(".")[0]}.mp4'
	retVal = subprocess.call(cmd, shell=True,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.STDOUT)
	if retVal == 0:
		return True
	return False

def muxTracks(video,audio):
	cmd = f'ffmpeg -an -i temp/{video} -vn -i temp/{audio} -r 30 -acodec copy -vcodec copy output/{video.split("-")[1].split(".")[0]}.mp4'
	retVal = subprocess.call(cmd, shell=True, 
		stdout=subprocess.DEVNULL, 
		stderr=subprocess.STDOUT)
	if retVal == 0:
		return True
	return False

def autoCombine(video,audio):
	if video.split(".")[1] != "mp4":
		if toMP4(video) == False:
			return False
		video = video.split(".")[0] + ".mp4"
	if toMP4(audio) == False:
		return False
	audio = audio.split(".")[0] + ".mp4"

	if muxTracks(video,audio) == False:
		return False
	return True

if __name__ == "__main__":
	result = autoCombine("video-mfPCFQfOnLg.mp4","audio-mfPCFQfOnLg.webm")
	print(result)