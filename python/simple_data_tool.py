import json


class SimpleDataTool:
    JSON_FILENAME_SIMPLE = "simple.json"

    def load_simple_models(self):
        simple_models = None

        with open(self.JSON_FILENAME_SIMPLE, 'r', encoding='utf-8') as file:
            simple_models = json.load(file)

        return simple_models
