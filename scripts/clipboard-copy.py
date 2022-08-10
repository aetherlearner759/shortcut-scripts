import argparse
import os
import json
import pyperclip

from helperutils import GetResponse 
"""
Saves text files into disk that you can copy into clipboard by commands.
"""

# Define the command-line arguments for this script
def getArgumentParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('mode', default="copy", nargs='?', choices=["copy", "save", "remove"], help="'copy' to copy text into clipboard. 'save' to save text into file. 'remove' to remove key")
	parser.add_argument('-key', default=None, help="Key of the text to copy or save")
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
	main()