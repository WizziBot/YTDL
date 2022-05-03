import re

text = "video-Interview with an Agile Coach in 2022 - Sprint2.mp4"
# result = re.search("^video-(.*)",text).group(1)
result = "-".join(text.split("-")[1:])
print(result)

