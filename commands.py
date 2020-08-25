import os
import shutil
import json
import subprocess
from utils import BlogError, new_dir, new_file, clear_dir, flatten, git
from generate import generate_html

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
        config = { 
            'blog_title': 'My awesome Octoblog',
            'url': 'https://[YOUR_USERNAME].github.io',
            'theme': 'default',
            'category_display_names': {
                'articles': 'All Articles',
            },
            'menu_items': [
                {
                    'title': 'Blog',
                    'page': 'HOME',
                },
                {
                    'title': 'About',
                    'page': 'pages/about.md',
                },
            ],
        }
        new_file('config.json', json.dumps(config, indent=4))

        new_dir('articles')
        new_file('articles/welcome.md', '''# Welcome 
This is my personal tiny island in the ocean that is the world wide web.''')
        new_dir('pages')
        new_file('pages/about.md', '''# About me
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

class CloneCommand:
    def __init__(self, remote):
        git(['clone', remote, '.'])
        git(['checkout', 'dev'])

class SaveCommand:
    def __init__(self):
        print('---> saving to github')
        git(['pull', '--allow-unrelated-history', 'origin', 'dev'])
        git(['add', '.'])
        git(['commit', '-m', 'octoblog-save'])
        git(['push', 'origin', 'dev'])
        print('---> done')

class PreviewCommand:
    def __init__(self):
        os.makedirs('preview', exist_ok=True)
        clear_dir('preview')
        config = json.load(open('config.json', 'r'))
        config['url'] = 'file:///' + os.getcwd() + '/preview'
        generate_html(config, 'preview')

class PublishCommand:
    def __init__(self):
        git(['checkout', 'master'])
        git(['commit', '--allow-empty', '-m', 'octoblog-publish notification'])
        git(['checkout', 'dev'])


        print('---> generating blog to www/ directory')
        clear_dir('www')
        config = json.load(open('config.json', 'r'))
        generate_html(config, 'www')
        print('---> done')

        SaveCommand()

        print('---> pushing contents of www/ to master')
        git(['checkout', 'master'])
        clear_dir(os.getcwd())
        git(['checkout', 'dev', '--', 'www'])
        flatten('www')
        git(['add', '.'])
        git(['commit', '-m', '"octoblog-publish files"'])
        git(['push', 'origin', 'master'])
        git(['checkout', 'dev'])
        print('---> done')
