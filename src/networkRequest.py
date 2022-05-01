from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import re
import os

# Returns Links we need
def getLinks(origUrl):

	# Enable Performance Logging of Chrome.
	desired_capabilities = DesiredCapabilities.CHROME
	desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

	options = webdriver.ChromeOptions()
	# Uncomment for setting to your own browser context, however might delete all your extensions, make a backup incase (..\User Data\Default\Extensions)
	# profilePath = os.path.expanduser("~")+r'\AppData\Local\Google\Chrome\User Data'
	# options.add_argument("user-data-dir="+profilePath)
	options.add_argument('log-level=3') # annoying console notis
	options.add_argument("--ignore-certificate-errors")

	driver = webdriver.Chrome(executable_path="C:/chromedriver.exe",
							chrome_options=options,
							desired_capabilities=desired_capabilities)

	# REQUEST
	driver.get(origUrl)
	time.sleep(15)
	logs = driver.get_log("performance")

	# network_log.json
	with open("temp/network_log.json", "w", encoding="utf-8") as f:
		f.write("[")

		# Iterates every logs and parses it using JSON
		for log in logs:
			network_log = json.loads(log["message"])["message"]
			if("Network.response" in network_log["method"]
                    or "Network.request" in network_log["method"]
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
				if float(xre.group(4)) < 60.0:
					continue
				# print("ITAG:",xre.group(1))
				links.append((xre.string,xre.group(2),xre.group(3),xre.group(1)))
				if len(links) >=6:
					links.pop(0)
		except Exception as e:
			pass
	return links

if __name__ == "__main__":
	lnks = getLinks("https://www.youtube.com/watch?v=mfPCFQfOnLg")
	for li in lnks:
		print(li[0][:30],"   :   ",li[1],li[2],end="\n\n")