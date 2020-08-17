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
            'home_template': 'home.template.html',
            'article_template': 'article.template.html',
            'index_template': 'index.template.html',

            'articles': {
                'display_name': 'All Articles',
            },
        }
        new_file('config.json', json.dumps(config, indent=4))

        new_dir('articles')
        new_file('articles/welcome.md', '''# Welcome 
This is my personal tiny island in the ocean that is the world wide web.''')
        new_dir('www')
        new_dir('preview')
        new_file('.gitignore', '''preview/''')

        # copy default files from script execution dir
        defaults_dir = os.path.join(os.path.dirname(__file__), 'default')
        new_dir('templates')
        shutil.copy(os.path.join(defaults_dir, 'templates', 'base.template.html'), 'templates')
        shutil.copy(os.path.join(defaults_dir, 'templates', 'parent_tree.template.html'), 'templates')
        shutil.copy(os.path.join(defaults_dir, 'templates', 'list_of_articles.template.html'), 'templates')
        shutil.copy(os.path.join(defaults_dir, 'templates', 'home.template.html'), 'templates')
        shutil.copy(os.path.join(defaults_dir, 'templates', 'article.template.html'), 'templates')
        shutil.copy(os.path.join(defaults_dir, 'templates', 'index.template.html'), 'templates')
        
        new_dir('assets')
        shutil.copy(os.path.join(defaults_dir, 'assets', 'style.css'), 'assets')
        
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
