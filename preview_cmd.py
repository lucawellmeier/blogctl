import json
from generate import generate

class PreviewCommand:
    def __init__(self):
        config = json.load(open('config.json', 'r'))
        config['url'] = ''
        generate('preview', config)
