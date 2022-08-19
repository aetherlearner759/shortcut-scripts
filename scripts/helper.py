
# A class that gets a selection from the choices out of the user
class GetResponse:
    def __init__(self, choices=["Y", "N"], case_sensitive=False, stripResponse=True):
        self.choices = choices.copy()
        self.case_sensitive = case_sensitive
        self.stripResponse = stripResponse
    
    def input(self, prompt=None):
        while True:
            # Get response from user
            resp = ""
            if prompt is None:
                resp = input(f"Choose ({' or '.join(self.choices)})  ")
            else:
                resp = input(prompt)
            
            # Process response 
            if self.stripResponse:
                resp = resp.strip()
            
            for choice in self.choices:
                if (self.case_sensitive and choice == resp) or (not self.case_sensitive and choice.lower() == resp.lower()):
                    return resp 
        return
    

import tempfile 
import os
import subprocess

# Prompts for user text input by opening a temporary file in the default text editor
class PromptEditor:
    def __init__(self, initial_content=""):
        if not isinstance(initial_content, str):
            raise TypeError("Given initial content must be a string")
        
        self.DEFAULTEDITOR = os.environ.get('EDITOR', 'Notepad')
        self.initial_content = initial_content 
        return
    
    def prompt(self, prompt=""):
        if not isinstance(prompt, str):
            raise TypeError("Given prompt must be a string")
        if prompt != "":
            print(prompt)
        result = ""
        try:
            # Create temporary file and set initial content
            with tempfile.NamedTemporaryFile(dir=os.path.dirname(__file__)+"\\..\\.temp", suffix=".tmp", delete=False) as tempFile:
                tempFile.write(str.encode(self.initial_content))
                tempFile.flush()
            # Open default text editor 
            subprocess.run([self.DEFAULTEDITOR, tempFile.name])
            # Get user input and cleanup
            with open(tempFile.name, 'r') as userInput:
                result = userInput.read()
        finally:
            if tempFile.name is not None:
                os.remove(tempFile.name)
            
        return result