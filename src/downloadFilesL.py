import asyncio
import os.path
import shutil
import time
import aiofiles
import aiohttp
from tempfile import TemporaryDirectory


async def get_content_length(url):
	async with aiohttp.ClientSession() as session:
		async with session.head(url) as request:
			# print(request)
			# print(request.content_length)
			return request.content_length


def parts_generator(size, start=0, part_size=10 * 1024 ** 2):
	while size - start > part_size:
		# print(f'{size}-{start} vs {part_size}')
		yield start, start + part_size
		start += part_size
	yield start, size


async def download(url, headers, save_path):
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as request:
			file = await aiofiles.open(save_path, 'wb')
			await file.write(await request.content.read())

async def process(target,outDir):
	url = target[0]
	filename = target[1]
	if url == "":
		return
	tmp_dir = TemporaryDirectory(prefix=filename, dir=os.path.abspath('.'))
	size = await get_content_length(url)
	tasks = []
	file_parts = []
	for number, sizes in enumerate(parts_generator(size+1,start=0)):
		part_file_name = os.path.join(tmp_dir.name, f'{filename}.part{number}')
		file_parts.append(part_file_name)
		print(f'Processing: {round((sizes[0] / size)*100)}%')
		tasks.append(download(url, {'Range': f'bytes={sizes[0]}-{sizes[1]-1}'}, part_file_name))
	print('Processing: 100%\n')
	print('Generating File...\n')
	await asyncio.gather(*tasks)
	with open(outDir+filename, 'wb') as wfd:
		length = len(file_parts)
		for i,f in enumerate(file_parts):
			print(f'Downloading: {round(((i+1) / length)*100)}%')
			with open(f, 'rb') as fd:
				shutil.copyfileobj(fd, wfd)


async def main(urls,outDir):
	if len(urls) < 1:
		return
	await asyncio.gather(*[process(url,outDir) for url in urls])
	
def chEx(path):
	if not os.path.isdir(path):
		os.mkdir(path)

async def downloadUrls(urls,outDir):
	# loop = asyncio.get_event_loop()
	# loop.run_until_complete(main(urls,outDir))
	path = os.path.join(os.path.abspath("."), outDir)
	chEx(path)
	path = os.path.join(os.path.abspath("."), "temp")
	chEx(path)
	await main(urls,outDir)

if __name__ == '__main__':

	start_code = time.monotonic()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(downloadUrls([("https://rr3---sn-8pgbpohxqp5-ac56.googlevideo.com/videoplayback?expire=1651806806&ei=9T10YpW_OYPZsAKtqK6AAw&ip=81.101.41.153&id=o-AAs_wyHIgRVF0PADEPRqj6NpSpyH6pnVtBMBtgldKYSY&itag=399&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278%2C394%2C395%2C396%2C397%2C398%2C399&source=youtube&requiressl=yes&mh=ip&mm=31%2C29&mn=sn-8pgbpohxqp5-ac56%2Csn-aigl6nsr&ms=au%2Crdu&mv=m&mvi=3&pl=22&initcwndbps=1161250&spc=4ocVC759ATAZ4I5IF58UOuEL2ltsb0VYPEvNMgVs8Q&vprv=1&mime=video%2Fmp4&ns=0YPfTLvF_KeYao1PGbIAPAUG&gir=yes&clen=213479536&dur=773.083&lmt=1633267841347528&mt=1651784947&fvip=4&keepalive=yes&fexp=24001373%2C24007246&c=WEB&txp=1436434&n=sXIHzGHSVJ1WfQ&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cspc%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAPP-u0wkALXsLJ3y_hDK7VKOKWyIePWR30djEDv6jydFAiB7fLOQmoFx78Aq2qod_xIJrPb5EYXm9v-SP58CHmTBEQ%3D%3D&alr=yes&sig=AOq0QJ8wRQIgDoIIKjBOnQYL1H_Uo7iVV1e0fc8unHIbrqxzT3JTV-QCIQDR5Y_DSA8VbVW7zzgn6D71EG2Gv6hqm-N0m8Wm4DRLng%3D%3D&cpn=oolZUMeab8laYns0&cver=2.20220502.01.00","100zp.webm")],"tests2/"))
	print(f'{time.monotonic() - start_code} seconds!')