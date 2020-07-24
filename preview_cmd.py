import os
import json
from generate import generate
from utils import cleardir

class PreviewCommand:
    def __init__(self):
        cleardir('preview')
        config = json.load(open('config.json', 'r'))
        config['url'] = ''
        generate('preview', config)
