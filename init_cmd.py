import os
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
        self._freshBlogPush(remote)
        print('---> done')

        print('---> generating preview')
        PreviewCommand()
        print('---> done')

        print('blog successfully initialized')

    def _create_base_structure(self):
        config = { 'blog_title': 'My awesome blog',
                'url': 'https://dummy.example.com',
                'article_template': 'article.template.html',
                'home_template': 'home.template.html' }
        new_file('config.json', json.dumps(config, indent=4))
        new_file('.gitignore', '''preview/''')
        new_dir('templates')
        new_file('templates/base.template.html', '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{% block head %}{% endblock %}
</head>
<body>
{% block main %}{% endblock %}
</body>
</html>''')
        new_file('templates/article.template.html', '''{% extends "base.template.html" %}
{% block head %}
<title> {{article.title}} | {{blog.title}} </title>
{% endblock %}
{% block main %}
<a href="{{article.path_to_root}}/index.html">back to home</a>
{{article.content}}
{% endblock %}''')
        new_file('templates/home.template.html', '''{% extends "base.template.html" %}
{% block head %}
<title> {{blog.title}} </title>
{% endblock %}
{% block main %}
<h1> {{blog.title}} </h1>
{% for article in blog.articles %}
<div> {{article.changes[-1]}} <a href="{{article.url}}">{{article.title}}</a> </div>
{% endfor %}
{% endblock %}''')
        new_dir('assets')
        new_dir('articles')
        new_file('articles/welcome.md', '''# Welcome 
This is my personal tiny island in the ocean that is the world wide web.''')
        new_dir('www')
        new_dir('preview')

    def _freshBlogPush(self, remote):
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
