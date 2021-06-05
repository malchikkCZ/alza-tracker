import json


class FileManager:

    def __init__(self):
        self.path = "./data.json"

    def load(self):
        try:
            with open(self.path) as file:
                items = json.load(file)
        except FileNotFoundError:
            items = []
        return items

    def save(self, data):
        print("Saving data.")
        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)
