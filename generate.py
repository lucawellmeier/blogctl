import os
import shutil
import markdown2
from jinja2 import Environment, FileSystemLoader
from template_globals import get_globals
from utils import HTMLTitleFinder, find_all_commits_for


###############################################
## find metadata for articles and categories ##
###############################################

def index_blog_structure(config):
    articles = []
    categories = []

    for root, sub_dirs, files in os.walk('articles', topdown=True):
        cur_category = find_category_meta(config, root)
        categories.append(cur_category)
        
        for filename in files:
            article = find_article_meta(config, os.path.join(root, filename))
            articles.append(article)

    return articles, categories

def find_category_meta(config, path):
    meta = {}
    meta['name'] = path
    meta['display_name'] = config[meta[path]]['display_name'] if 'name' in config and 'display_name' in config['name'] else meta['name']
    return {**meta, **find_link_info(config, path)}

def find_article_meta(config, path):
    meta = {}

    article_html = markdown2.markdown(open(path, 'r').read())
    title_finder = HTMLTitleFinder(article_html)
    meta['title'] = title_finder.headline
    meta['description'] = title_finder.first_paragraph
    meta['content'] = article_html
    meta['changes'] = find_all_commits_for(path)
    return {**meta, **find_link_info(config, path)}

def find_link_info(config, path):
    file_path = ''
    if os.path.isfile(path):
        file_path = os.path.splitext(path)[0] + '.html'
        dir_path = os.path.basename(path)
    if os.path.isdir(path):
        dir_path = path
        file_path = '/'.join([dir_path, 'index.html'])
    
    link_info = {}
    link_info['link'] = file_path
    link_info['root_dir'] = '/'.join(len(dir_path.split('/')) * ['..'])
    link_info['home_link'] = '/'.join([link_info['root_dir'], 'index.html'])

    return link_info

#################################################
## translate templated markdown code into html ##
#################################################

def generate_html(config, output_dir):
    articles, categories = index_blog_structure(config)
    
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.globals = get_globals(config, articles, categories)

    generate_home(config, output_dir, env)

    for category in categories:
        generate_category_index(config, output_dir, env, category) 
    
    for article in articles:
        generate_article(config, output_dir, env, article)
    
    copy_assets(output_dir)

def generate_home(config, output_dir, environment):
    template = environment.get_template(config['home_template'])
    html = template.render()

    export_path = os.path.join(output_dir, 'index.html')
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(html)

def generate_category_index(config, output_dir, environment, category):
    template = environment.get_template(config['index_template'])
    html = template.render(this=category)

    export_path = os.path.join(output_dir, category['link'])
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(html)

def generate_article(config, output_dir, environment, article):
    template = environment.get_template(config['article_template'])
    first_pass = template.render(this=article)
    second_pass = environment.from_string(first_pass).render()

    export_path = os.path.join(output_dir, article['link'])
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(second_pass)

def copy_assets(output_dir):
    export_path = os.path.join(output_dir, 'assets')
    os.makedirs(export_path)
    
    if os.path.exists(export_path):
        shutil.rmtree(export_path)

    shutil.copytree('assets', export_path)
