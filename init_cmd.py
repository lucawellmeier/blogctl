import os
import json
import subprocess
from utils import CustomError, newdir, newfile, git
from preview_cmd import PreviewCommand

class InitCommand:
    def __init__(self, remote):
        print('---> creating base structure')
        self._createBaseStructure()
        print('---> done')

        print('---> initial commit and push to server')
        self._freshBlogPush(remote)
        print('---> done')

        print('---> generating preview')
        PreviewCommand()
        print('---> done')

        print('blog successfully initialized')

    def _createBaseStructure(self):
        configDict = { 'blog_title': 'My awesome blog',
                'url': 'https://dummy.example.com',
                'article_template': 'article.template.html',
                'home_template': 'home.template.html' }
        newfile('config.json', json.dumps(configDict, indent=4))
        newfile('.gitignore', '''preview/''')
        newdir('templates')
        newfile('templates/base.template.html', '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{% block head %}{% endblock %}
</head>
<body>
{% block main %}{% endblock %}
</body>
</html>''')
        newfile('templates/article.template.html', '''{% extends "base.template.html" %}
{% block head %}
<title> {{article.title}} | {{blog.title}} </title>
{% endblock %}
{% block main %}
<a href="{{article.path_to_home}}/index.html">back to home</a>
{{article.content}}
{% endblock %}''')
        newfile('templates/home.template.html', '''{% extends "base.template.html" %}
{% block head %}
<title> {{blog.title}} </title>
{% endblock %}
{% block main %}
<h1> {{blog.title}} </h1>
{% for article in blog.articles %}
<div> {{article.changes[-1]}} <a href="{{article.url}}">{{article.title}}</a> </div>
{% endfor %}
{% endblock %}''')
        newdir('articles')
        newfile('articles/welcome.md', '''# Welcome 
This is my personal tiny island in the ocean that is the world wide web.''')
        newdir('www')
        newdir('preview')

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
