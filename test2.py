import asyncio

def mainloop(smthcb,loop):
	asyncio.set_event_loop(loop)
	status = loop.run_until_complete(main(True,smthcb))
	print("STATUS")
	print(status)
	loop.close()

async def main(isGUI,callback):
	for i in range(4):
		comb = ""
		if True:
			if isGUI:
				print("\nCombine Audio and Video? [y/n]")
				# insert callback here (will contain rest of main)
				response = await callback()
				print("RESPONSE")
				print(response)
				comb = response
			else:
				comb = input("\nCombine Audio and Video? [y/n]: ")
				print()
		if comb == "y":
			print("COMB YES")
		elif comb == "n":
			print("COMB NO")
		else:
			print("EXITING")
			exit(1)
			
	print("\n----DONE----\n")
	return "HELLO"