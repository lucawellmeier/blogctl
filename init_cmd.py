import os
import subprocess
from utils import newdir, newfile, git

class InitCommand:
    def __init__(self):
        self._createBaseStructure()
        self._pushToGit()

    def _createBaseStructure(self):
        newfile('config.json', '''{
    "blog_title": "My awesome blog",
    "articles_root": {
        "dir": "articles",
        "display_name": "Home",
        "index_default_template": "templates/index.html",
        "article_default_template": "templates/article.html",
        "subdirs": [
            {
                "dir": "test",
                "display_name": "Tests"
            }
        ]
    }
}''')
        newfile('.gitignore', '''preview/''')
        newdir('templates')
        newfile('templates/base.html', '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{% block head %}{% endblock %}
</head>
<body>
{% block main %}{% endblock %}
</body>
</html>''')
        newfile('templates/article.html', '''{% extends "templates/base.html" %}
{% block head %}
<title> {{current_article.title}} | {{blogname}} </title>
{% endblock %}
{% block main %}
{{ ['<a href="' + node.link + '">' + node.name + '</a>' for node in current_directory.path] | join(' &gt; ') }}
{{content}}
{% endblock %}''')
        newfile('templates/index.html', '''{% extends "templates/base.html" %}
{% block head %}
<title> {{ (current_directory).title }} | {{blogname}} </title>
{% endblock %}
{% block main %}
<h1> {{ (current_directory).title }} </h1>
{% for subdir in current_directory.subdirs %}
<a href="{{subdir.link}}">{{subdir.name}}</a>
{% endfor %}
<br>
{% for article in articles %}
{{article.last_change_date}} <a href="{{article.link}}">{{article.name}}</a>
{% endfor %}
{% endblock %}''')
        newdir('articles')
        newfile('articles/welcome.md', '''# Welcome 
This is my personal tiny island in the ocean that is the world wide web.''')
        newdir('articles/test')
        newfile('articles/test/directory_test.md', '''## Directory Test
Well... This proves that directories work in this tool''')
        newdir('docs')
        newdir('preview')

def _pushToGit(self):
    git(['commit', '-a', '-m', '"setup blog file structure"'])
