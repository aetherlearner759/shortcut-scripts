import argparse
import os
import json
import pyperclip

from helper import GetResponse, PromptEditor
"""
Saves text files into disk that you can copy into clipboard by commands.
"""
def is_valid_clipboard_key(key):
    for c in key:
        if c.isspace():
            return False 
    return True
    
# Copy text to clipboard
def copy_text_from_store(args, textstore):
	key = args.key
	if key is None:
		key = input("What is the key of the text you want to copy?  ").strip()
	
	while True:
		if textstore.has(key):
			text = textstore.get(key)
			pyperclip.copy(text)
			print("Pasted text to your clipboard")
			break
		else:
			key = input(f"Unable to find key: {key}\nRetype the key (Or enter nothing to quit) ").strip()
			if key == "":
				break
	return

# Save text to file to copy into clipboard later 
def save_text_to_store(args, textstore):
	key = args.key
	while True:
		if key is None:
			key = input("Set the key of the text. (Enter empty to quit)  ").strip()
		if key == "":
			break
		if not is_valid_clipboard_key(key):
			print("Key cannot have a whitespace")
			continue
		if textstore.has(key):
			print("Key alread yexist")
			# TODO: If key is already being used, ask for user if they are okay to overwrite, change current key, change the existing key, or quit

		text = ""
		if args.frominput == "edit":
			message = 	"Replace this text with the text you want to save. When you are done, save this file and close.\n[Save an empty file to terminate or close the file without modifying anything]"
			editor = PromptEditor(message)
			text = editor.prompt()

			if text == "" or text == message:
				print("Terminating save.")
				return
		elif args.frominput == "clip":
			text = pyperclip.paste()
   
			if text == "":
				print("No text saved within clipboard. Please try again.")
				return
		elif args.frominput == "file":
			filePath = input("Please input a file path: ")
			with open(filePath, 'r') as inputFile:
				text = inputFile.read()
    
			if text == "":
				print("Empty file. Please try again.")
				return
		else:
			print(f"Unknown form of input {args.frominput}")
			return

  		# Prompt for confirmation
		print("\nIs this okay to save?\n")
		print(f"Key: {key}")
		print(f"Text:\n{text}")

		resp = GetResponse(choices=["Y", "N"]).input("(Y or N)  ")
		if resp == "Y":
			textstore.set(key, text)
			# Prompt for next action
			resp = GetResponse(choices=["S", "C", "Q"]).input("Type S to save another. Type C to copy. Type Q to quit.  ")
			if resp == "S":
				key = None
				continue
			elif resp == "C":
				copy_text_from_store(args, textstore)
				break
			elif resp == "Q":
				break
		elif resp == "N":
			key = None
			continue
	return 

def remove_text_from_store(args, textstore):
    print(args)
    pass

def list_key_from_store(args, textstore):
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

# Remove key 
def remove_mode(Args, TextStore):
	# TODO: implement this
	pass






def main():
	args = getArgumentParser()
	textstore = ClipBoardStore()
	args = args.parse_args()
 
	if args.handle is None:
		print(f"Unknown mode {args.mode}")
		return 
	args.handle(args, textstore)
	return
	

if __name__ == "__main__":
	main()