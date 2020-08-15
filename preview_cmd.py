import os
import json
from generate import generate_html
from utils import clear_dir

class PreviewCommand:
    def __init__(self):
        os.makedirs('preview', exist_ok=True)
        clear_dir('preview')
        config = json.load(open('config.json', 'r'))
        config['url'] = 'file:///' + os.getcwd() + '/preview'
        generate_html(config, 'preview')
