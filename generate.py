import os
import shutil
import re
from datetime import datetime
from html.parser import HTMLParser
import markdown2
from jinja2 import Environment, FileSystemLoader
from utils import CustomError, git

class HeadlineFinder(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self._headlineTags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        self._foundHeadline = False
        self._currentHeadlineType = None
        self._titleBuffer = ''
        self.title = ''

        self.feed(html)

    def handle_starttag(self, tag, attr):
        if tag in self._headlineTags and not self._foundHeadline:
            self._foundHeadline = True
            self._currentHeadlineType = tag

    def handle_data(self, data):
        self._titleBuffer += data
    
    def handle_endtag(self, tag):
        if self._foundHeadline and self._currentHeadlineType == tag:
            self.title = self._titleBuffer

def findGitChangesFor(article_file):
    log = git(['log', '--follow', '--', article_file])
    lines = log.splitlines(keepends=True)

    commit_parts = []
    for line in lines:
        if re.match('^commit', line):
            commit_parts.append([line])
        elif len(commit_parts) > 0:
            commit_parts[-1] += [line]

    raw_date_lines = [commit[2] for commit in commit_parts if len(commit) >= 3]
    stripped_date_lines = [re.match(r'^\s*Date:\s*(.+)\s*$', line).group(1) 
            for line in raw_date_lines]
    datetimes = sorted([datetime.strptime(datestr, '%c %z') for datestr in stripped_date_lines])
    return [dt.strftime('%c %Z') for dt in datetimes]

def findArticleMeta(article_file, category, config):
    articleMeta = {}

    articleMeta['category'] = category
    articleMeta['export_file'] = os.path.splitext(article_file)[0] + '.html'
    articleMeta['path_from_root'] = articleMeta['export_file']
    with open(os.path.join(article_file), 'r') as f:
        articleMeta['content'] = markdown2.markdown(f.read())

    headlineFinder = HeadlineFinder(articleMeta['content'])
    if not headlineFinder.title:
        raise CustomError('no headline found in article ' + articleFile)
    articleMeta['title'] = headlineFinder.title

    articleMeta['changes'] = findGitChangesFor(article_file)
    return articleMeta

def exportArticle(articleMeta, outputDir, config, blogInfo, tools):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    env.globals['blog'] = blogInfo
    env.globals['tools'] = tools
    env.globals['category'] = articleMeta['category']

    parts = articleMeta['category']['name'].split('/')
    env.globals['path_to_root'] = '/'.join((len(parts)) * ['..'])
    env.globals['path_to_assets'] = os.path.join(env.globals['path_to_root'], 'assets')
    env.globals['path_from_root'] = articleMeta['export_file']

    env.globals['article_content'] = env.from_string(articleMeta['content']).render()
    del articleMeta['content']
    env.globals['article'] = articleMeta

    template = env.get_template(config['article_template'])
    html = template.render()
    
    path = os.path.join(outputDir, articleMeta['export_file'])
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, 'w') as f:
        f.write(html)

def exportCategoryIndex(categoryMeta, outputDir, config, blogInfo, tools):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.globals['blog'] = blogInfo
    env.globals['tools'] = tools
    env.globals['category'] = categoryMeta

    parts = categoryMeta['name'].split('/')
    env.globals['path_to_root'] = '/'.join((len(parts)) * ['..'])
    env.globals['path_to_assets'] = os.path.join(env.globals['path_to_root'], 'assets')

    template = env.get_template(config['index_template'])
    html = template.render()

    path = os.path.join(outputDir, categoryMeta['path_from_root'], 'index.html')
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, 'w') as f:
        f.write(html)

def exportHome(outputDir, config, blogInfo, tools):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.globals['blog'] = blogInfo
    env.globals['tools'] = tools
    env.globals['path_to_root'] = '.'
    env.globals['path_to_assets'] = os.path.join(env.globals['path_to_root'], 'assets')
    template = env.get_template(config['home_template'])
    html = template.render()

    path = os.path.join(outputDir, 'index.html')
    with open(path, 'w') as f:
        f.write(html)

def find_single_category_meta(cat_name, all_cat_names, config):
    meta = {}
    meta['name'] = cat_name
    meta['display_name'] = config[meta['name']]['display_name'] if 'name' in config and 'display_name' in config['name'] else meta['name']
    meta['path_from_root'] = cat_name

    meta['parents'] = []
    parts = cat_name.split('/')
    for i in range(0, len(parts) - 1):
        meta['parents'].append('/'.join(parts[0:i + 1]))

    meta['children'] = []
    for other in all_cat_names:
        if other.startswith(cat_name) and len(other.split('/')) == len(parts) + 1:
            meta['children'].append(other)

    return meta

def generate(outputDir, config):
    all_cat_names = []
    for root, dirs, files in os.walk('articles'):
        if root not in all_cat_names:
            all_cat_names.append(root)

    categories = []
    articles = []
    for root, dirs, files in os.walk('articles'):
        for f in files:
            if os.path.splitext(f)[1] == '.md':
                category = find_single_category_meta(root, all_cat_names, config)
                if category['name'] not in [c['name'] for c in categories]:
                    categories.append(category)

                path = os.path.join(root, f)
                meta = findArticleMeta(path, category, config)
                articles.append(meta)

    blogInfo = {}
    blogInfo['title'] = config['blog_title']
    blogInfo['url'] = config['url']
    blogInfo['articles'] = articles
    blogInfo['categories'] = categories

    tools = {}
    tools['getcat'] = lambda name : [c for c in categories if c['name'] == name][0]
    tools['getartsforcat'] = lambda cat : [a for a in articles if a['category']['name'].startswith(cat['name'])]

    for root, dirs, files in os.walk('assets'):
        for f in files:
            src = os.path.join(root, f)
            destDir = os.path.join(outputDir, root)
            dest = os.path.join(destDir, f)
            os.makedirs(os.path.join(destDir), exist_ok=True)
            shutil.copyfile(src, dest)
    for article in articles:
        exportArticle(article, outputDir, config, blogInfo, tools)
    for category in categories:
        exportCategoryIndex(category, outputDir, config, blogInfo, tools)
    exportHome(outputDir, config, blogInfo, tools)
