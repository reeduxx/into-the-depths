import textwrap

class Class:
    def __init__(self, class_data):
        self.name = class_data["name"]
        self.description = class_data["description"]
    
    def __str__(self, wrap_width):
        wrapped_description = '\n'.join(textwrap.fill(self.description, width=wrap_width).split('\n'))
        return f"{self.name}\n{wrapped_description}"