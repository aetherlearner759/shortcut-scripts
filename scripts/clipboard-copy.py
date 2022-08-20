import argparse
import os
import json
import pyperclip

from helper import GetResponse 
"""
Saves text files into disk that you can copy into clipboard by commands.
"""

def copy_text_from_store(args):
    print(args)
    pass

def save_text_to_store(args):
    print(args)
    pass

def remove_text_from_store(args):
    print(args)
    pass

def list_key_from_store(args):
    print(args)
    pass

# Define the command-line arguments for this script
def getArgumentParser():
	parser = argparse.ArgumentParser(
		description="Manages a store of text that can be copied to the clipboard given a key.",
		add_help=True,
		allow_abbrev=True,
		exit_on_error=True
	)
	subparser = parser.add_subparsers(
		metavar="MODE", 
		help="Specify which operation to perform",
		required=True
	)
	# copy subcommand
	copy_parser = subparser.add_parser(
		"copy", aliases=['cp'],
		help="Copy text into clipboard."
	)
	copy_parser.add_argument(
		"key", nargs="?", default=None, type=str,
		help="Key of the text to save. Key must have no whitespace."
	)
	copy_parser.set_defaults(handle=copy_text_from_store)
	# save subcommand
	save_parser = subparser.add_parser(
		"save", aliases=['sv'],
		help="Save text to copy into clipboard later."
	)
	save_parser.add_argument(
		"key", nargs="?", default=None, type=str,
		help="Key of the text to save. Key must have no whitespace."
	)
	save_parser.add_argument(
     	"-from", default="edit", choices=["edit", "clip", "file"], dest="frominput",
		help="Where to get the text from. 'edit' (default) by opening an editor, 'clip' from clipboard, 'file' from text file in given file path."
	)
	save_parser.set_defaults(handle=save_text_to_store)
	# remove subcommand
	remove_parser = subparser.add_parser(
		"remove", aliases=['rm'],
		help="Remove saved text."
	)
	remove_parser.add_argument(
		"key", nargs="?", default=None, type=str,
		help="Key of the text to save. Key must have no whitespace."
	)
	remove_parser.add_argument(
		"-confirm", action="store_true", 
		help="Prompt for confirmation."
	)
	remove_parser.set_defaults(handle=remove_text_from_store)
	# list subcommand
	list_parser = subparser.add_parser(
		"list",
		help="List all keys pointing to saved texts."
	)
	list_parser.add_argument(
		"name", nargs="?", default=None, type=str, 
		help="Name of the keys to search for. Accepts wildcards: *, ?. Don't provide name parameter to get all keys."
	)
	list_parser.set_defaults(handle=list_key_from_store)
	return parser


# Manages the saved clipboard text 
class ClipBoardStore:
	def __init__(self):
		self.dataPATH = os.path.dirname(__file__) + "\\..\\data\\clipboard-copy"
		with open(f"{self.dataPATH}\\keys.json", 'r') as keys_file:
			self.keys = json.load(keys_file)
		return


	def __nameTextFile(self, key):
		return f"{key}-text.txt"

	def __updateKeysFile(self, key):
		keysPath = f"{self.dataPATH}\\keys.json"
		# Make sure keys.json file is found
		if not os.path.exists(keysPath):
			raise FileNotFoundError(f"keys.json is not found in {keysPath}")
		# Update keys file
		if key is not None:
			with open(keysPath, 'w') as keys_file:
				json.dump(self.keys, keys_file)
		return

	def __updateTextFile(self, name, text):
		textPath = f"{self.dataPATH}\\text\\{name}"
		# Delete text file if text is None
		if os.path.exists(textPath) and text is None:
			os.remove(textPath)
		# Otherwise update text file
		else:
			with open(textPath, 'w') as text_file:
				text_file.write(text)
		return


	def has(self, key):
		return key in self.keys

	def get(self, key):
		if key in self.keys:
			with open(f"{self.dataPATH}\\text\\{self.keys[key]}", 'r') as text_file:
				text = text_file.read()
				return text
		else:
			return None

	def set(self, key, text=""):
		self.keys[key] = self.__nameTextFile(key)
		self.__updateKeysFile(key)
		self.__updateTextFile(self.keys[key], text)
		
	def remove(self, key):
		if self.has(key):
			del self.keys[key]
		self.__updateKeysFile(key)
		self.__updateTextFile(self.keys[key])



# Copy text to clipboard
def copy_mode(Args, TextStore):
	key = Args.key
	if key is None:
		key = input("What is the key of the text you want to copy?  ").strip()
	
	while True:
		if TextStore.has(key):
			text = TextStore.get(key)
			pyperclip.copy(text)
			print("Pasted text to your clipboard")
			break
		else:
			key = input("Unable to find key. Retype the key (Enter empty to quit) ").strip()
			if key == "":
				break
	return


# Remove key 
def remove_mode(Args, TextStore):
	# TODO: implement this
	pass


# Save text to file to copy into clipboard later 
def save_mode(Args, TextStore):
	key = Args.key
	while True:
		if key is None:
			key = input("Set the key of the text. (Enter empty to quit)  ").strip()
		if key == "":
			break
		# TODO: If key is already being used, ask for user if they are okay to overwrite, change current key, change the existing key, or quit

		# FIXME: bad way for termination
		# TODO: Have option to take text from saved text in clipboard with pyperclip.paste() by supplying a switch parameter in commandline
		# TODO: Instead of asking to type in text into terminal, open a text editor to type in text instead like Git
		print("Input text you want to save. (Type ; to stop)")
		lines = []
		while True:
			line = input()
			if line == ";":
				break
			lines.append(line)
		text = '\n'.join(lines)
		if text == "\n":
			break

		# Prompt for confirmation
		print("\nIs this okay to save?\n")
		print(f"Key: {key}")
		print(f"Text:\n {text}")

		resp = GetResponse(choices=["Y", "N"]).input("(Y or N)  ")
		if resp == "Y":
			TextStore.set(key, text)
			# Prompt for next action
			resp = GetResponse(choices=["S", "C", "Q"]).input("Type S to save another. Type C to copy. Type Q to quit.  ")
			if resp == "S":
				key = None
				continue
			elif resp == "C":
				copy_mode(Args, TextStore)
				break
			elif resp == "Q":
				break
			
		elif resp == "N":
			key = None
			continue
	return 



def main():
	Args = getArgumentParser()
	TextStore = ClipBoardStore()
	Args = Args.parse_args()

	if Args.mode == "copy":
		copy_mode(Args, TextStore)
	elif Args.mode == "save":
		save_mode(Args, TextStore)
	else:
		print(f"Unknown mode {Args.mode}")
	return
	

if __name__ == "__main__":
	#main()
	arg = getArgumentParser()
	arg = arg.parse_args()
	arg.handle(arg)
	#print(arg)