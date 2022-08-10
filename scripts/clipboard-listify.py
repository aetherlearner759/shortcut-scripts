import argparse
import codecs
import pyperclip

# Workaround to accept string values with spaces between them by enclosing quotation marks around them
class JoinToString(argparse.Action):
	def __init__(self, option_strings, dest, nargs, **kwargs):
		super().__init__(option_strings, dest, nargs, **kwargs)
	
	def __call__(self, parser, namespace, values, option_string=None):
		stringValue = ' '.join(values)
		# Strip the surrounding quotation marks
		if stringValue[0] == stringValue [-1] and (stringValue[0] == "'" or stringValue[0] == '"'):
			stringValue = stringValue[1:-1]
		# Decode the string to convert raw escape characters to actual characters
		stringValue = codecs.decode(stringValue, 'unicode_escape')
		setattr(namespace, self.dest, stringValue)


def getArgumentParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-sep', nargs='+', default='\n', action=JoinToString, help="Strings to use to seperate each list item")
	parser.add_argument('-prefix',  nargs='+', default=' ', action=JoinToString, help="What to prefix each list item with")
	parser.add_argument('-increment', action='store_true', help="Prepend each list item with an index")
	return parser


def main():
	Args = getArgumentParser()
	Args = Args.parse_args()

	# TODO: Have option to type in text to terminal instead of copying from clipboard
	textToListify = pyperclip.paste()
	lines = textToListify.split(Args.sep)
	for i in range(len(lines)):
		if lines[i] != "":
			lines[i] = Args.prefix+lines[i]
			if Args.increment:
				lines[i] = f"{i+1}.{lines[i]}"

	ListifiedText = '\n'.join(lines)
	pyperclip.copy(ListifiedText)
	print("Listified text")
	return


if __name__ == "__main__":
	main()