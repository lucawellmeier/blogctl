import os
import json
from generate import generate
from utils import cleardir
from save_cmd import SaveCommand

class PublishCommand:
    def __init__(self):
        print('---> generating blog to www/ directory')
        cleardir('www')
        config = json.load(open('config.json', 'r'))
        generate('www', config)
        print('---> done')
        SaveCommand()
