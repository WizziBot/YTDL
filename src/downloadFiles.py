import asyncio
import os.path
import shutil
import time
import aiofiles
import aiohttp
from tempfile import TemporaryDirectory
from urllib.parse import urlparse


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
	# print("SIZE:",size)
	tasks = []
	file_parts = []
	for number, sizes in enumerate(parts_generator(size+1)):
		part_file_name = os.path.join(tmp_dir.name, f'{filename}.part{number}')
		file_parts.append(part_file_name)
		print(f'Progress: {round((sizes[0] / size)*100)}%')
		tasks.append(download(url, {'Range': f'bytes={sizes[0]}-{sizes[1]-1}'}, part_file_name))
	print('Progress: 100%\n')
	print('Generating File...\n')
	await asyncio.gather(*tasks)
	with open(outDir+filename, 'wb') as wfd:
		length = len(file_parts)
		for i,f in enumerate(file_parts):
			print(f'Assembling: {round(((i+1) / length)*100)}%')
			with open(f, 'rb') as fd:
				shutil.copyfileobj(fd, wfd)


async def main(urls,outDir):
	if len(urls) < 1:
		return
	await asyncio.gather(*[process(url,outDir) for url in urls])

def downloadUrls(urls,outDir):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(urls,outDir))

if __name__ == '__main__':

	start_code = time.monotonic()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main([("http://ipv4.download.thinkbroadband.com/100MB.zip","100zp.zip")]))
	print(f'{time.monotonic() - start_code} seconds!')