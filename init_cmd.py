import os
import shutil
import json
import subprocess
from utils import BlogError, new_dir, new_file, git
from preview_cmd import PreviewCommand

class InitCommand:
    def __init__(self, remote):
        print('---> creating base structure')
        self._create_base_structure()
        print('---> done')

        print('---> initial commit and push to server')
        self._fresh_blog_push(remote)
        print('---> done')

        print('---> generating preview')
        PreviewCommand()
        print('---> done')

        print('blog successfully initialized')

    def _create_base_structure(self):
        config = { 'blog_title': 'My awesome Octoblog',
            'url': 'https://[YOUR_USERNAME].github.io',
            'theme': 'default',
            'category_display_names': {
                'articles': 'Others',
            },
            'files_to_ignore_in_queries': [
                'articles/about.md',
            ],
        }
        new_file('config.json', json.dumps(config, indent=4))

        new_dir('articles')
        new_file('articles/welcome.md', '''# Welcome 
This is my personal tiny island in the ocean that is the world wide web.''')
        new_file('articles/aboud.md', '''# About me
Here goes your personal information.''')
        new_dir('assets')
        new_dir('www')
        new_dir('preview')
        new_file('.gitignore', '''preview/''')

        # copy default theme from script execution dir
        themes_dir = os.path.join(os.path.dirname(__file__), 'themes')
        shutil.copy_tree(themes_dir, os.path.join(os.getcwd(), 'themes'))
        
    def _fresh_blog_push(self, remote):
        git(['init'])
        git(['add', '.gitignore'])
        git(['commit', '-m', '"initial commit"'])
        git(['remote', 'add', 'origin', remote])
        git(['push', '-u', 'origin', 'master'])

        git(['branch', 'dev'])
        git(['checkout', 'dev'])
        git(['add', '.'])
        git(['commit', '-m', '"initial commit"'])
        git(['push', '-u', 'origin', 'dev'])
