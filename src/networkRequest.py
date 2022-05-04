from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import re
## Read below
import os

def getLinks(origUrl,config):
	delay = 10
	retries = 3
	# Enable Performance Logging of Chrome.
	desired_capabilities = DesiredCapabilities.CHROME
	desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

	options = webdriver.ChromeOptions()
	if config["displayChrome"] != "yes":
		options.add_argument('headless')
		delay = 3
	else:
		## Uncomment for setting to your own browser context, however might delete all your extensions, make a backup incase (C:\Users\You\AppData\...\User Data\Default\Extensions)
		profilePath = os.path.expanduser("~")+r'\AppData\Local\Google\Chrome\User Data'
		options.add_argument("user-data-dir="+profilePath)
	options.add_argument('log-level=3') # annoying console notis
	options.add_argument("--ignore-certificate-errors")
	
	driver = webdriver.Chrome(executable_path="C:/chromedriver.exe",
							chrome_options=options,
							desired_capabilities=desired_capabilities)
	# REQUEST
	driver.get(origUrl)
	# Wait for ads and then erases browser data (avoid polluting the links with the ad media)
	time.sleep(2)
	isAds = driver.find_elements_by_css_selector('#player-overlay\:0')
	while len(isAds) > 0:
		# print("Halting for ads..")
		driver.get_log("performance")
		time.sleep(0.5)
		isAds = driver.find_elements_by_css_selector('#player-overlay\:0')

	time.sleep(delay)
	titleResults = driver.find_elements_by_css_selector('#container > h1 > yt-formatted-string')
	titleResults2 = driver.find_elements_by_css_selector('#title > h1 > yt-formatted-string')
	if len(titleResults2) > 0:
		titleResults= titleResults2
	title="default"
	if len(titleResults) == 0:
		title = re.search("v?=(.*)$",origUrl).group(1)
	elif titleResults[0].text == "":
		for _ in range(retries):
			time.sleep(1)
			titleResults = driver.find_elements_by_css_selector('#container > h1 > yt-formatted-string')
			titleResults2 = driver.find_elements_by_css_selector('#title > h1 > yt-formatted-string')
			if len(titleResults2) > 0:
				titleResults= titleResults2
			if titleResults[0].text != "":
				title = titleResults[0].text.replace(" ","_")
				break
	else:
		title = titleResults[0].text.replace(" ","_")
	logs = driver.get_log("performance")

	# network_log.json
	with open("temp/network_log.json", "w", encoding="utf-8") as f:
		f.write("[")

		# Iterates every logs and parses it using JSON
		for log in logs:
			network_log = json.loads(log["message"])["message"]
			if("Network.request" in network_log["method"]
                    or "Network.response" in network_log["method"]
                    or "Network.webSocket" in network_log["method"]):
				f.write(json.dumps(network_log)+",")
		f.write("{}]")

	driver.quit()

	json_file_path = "temp/network_log.json"
	with open(json_file_path, "r", encoding="utf-8") as f:
		logs = json.loads(f.read())

	# Iterate the logs
	links = []
	for log in logs:
		try:
			# URL
			url = log["params"]["request"]["url"]

			#RegExp
			xre = re.search("^https://rr[1|2|3|4|5]---sn-.*\.googlevideo\.com/videoplayback?.*itag=([0-9]*).*mime=(.*)%2F([a-z0-9]*).*&dur=([0-9]*\.[0-9]*)", url)
			if xre:
				links.append((xre.string,xre.group(2),xre.group(3),str(xre.group(1)),xre.group(4)))
				if len(links) >=10:
					links.pop(0)
		except Exception as e:
			pass
	os.remove(json_file_path)
	return title,links

if __name__ == "__main__":
	pass
	title,lnks = getLinks("https://www.youtube.com/watch?v=A-H-xZ5ZXgo",
	{"useYoutubeTitle":"yes",
		"downloadVideo":"yes",
		"downloadAudio":"yes",
		"outputVideoFormat":"mp4",
		"outputAudioFormat":"webm",
		"promptCombine":"no",
		"verbose":"no",
	})