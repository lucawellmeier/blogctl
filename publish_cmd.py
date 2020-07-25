import os
import json
from utils import cleardir, git, flatten
from generate import generate
from save_cmd import SaveCommand

class PublishCommand:
    def __init__(self):
        print('---> generating blog to www/ directory')
        cleardir('www')
        config = json.load(open('config.json', 'r'))
        generate('www', config)
        print('---> done')

        SaveCommand()

        print('---> pushing contents of www/ to master')
        git(['checkout', 'master'])
        cleardir(os.getcwd())
        git(['checkout', 'dev', '--', 'www'])
        flatten('www')
        git(['add', '.'])
        git(['commit', '-m', '"blogctl deploy"'])
        git(['push', 'origin', 'master'])
        git(['checkout', 'dev'])
        print('---> done')
