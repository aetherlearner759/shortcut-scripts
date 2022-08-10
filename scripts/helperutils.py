
# A class that gets response from user
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
            
            for choice in choices:
                if (self.case_sensitive and choice == resp) or (not self.case_sensitive and choice.lower() == resp.lower()):
                    return resp 
        return
    
