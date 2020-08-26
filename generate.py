import os
import shutil
import datetime
import calendar
import markdown2
from jinja2 import Environment, FileSystemLoader
from template_globals import get_globals
from utils import HTMLTitleFinder, find_dates, clear_dir


###############################################
## find metadata for articles and categories ##
###############################################

def index_blog_structure(config):
    articles = []
    categories = []
    months = []
    pages = []

    for root, sub_dirs, files in os.walk('articles', topdown=True):
        cur_category = find_category_meta(config, root)
        categories.append(cur_category)
        
        for filename in files:
            article = find_article_meta(config, os.path.join(root, filename))

            if article['changes']:
                publish_date = article['changes'][0]
                month = (publish_date.year, publish_date.month)

                if month not in [meta['month'] for meta in months]:
                    meta = {}
                    meta['collection_type'] = 'month'
                    meta['month'] = month
                    meta['start'] = datetime.datetime(month[0], month[1], 1).timestamp()
                    meta['end'] = meta['start'] + calendar.monthrange(*month)[1] * 24 * 60 * 60
                    meta['active_menu_item'] = 'BLOG_ARCHIVES'
                    meta['display_name'] = calendar.month_name[month[1]] + ' ' + str(month[0])

                    zero_padded = str(month[1]) if month[1] > 9 else '0' + str(month[1])
                    index_path = '/'.join(['archives', str(month[0]) + '_' + zero_padded + '.html'])
                    meta['path'] = index_path
                    meta['link'] = '/'.join([config['url'], index_path])
                    months.append(meta)

            articles.append(article)

    for root, sub_dirs, files in os.walk('pages', topdown=True):
        for filename in files:
            page = find_page_meta(config, os.path.join(root, filename))
            pages.append(page)

    articles = sorted(articles, key=lambda a:a['changes'][-1])
    categories = sorted(categories, key=lambda c:c['name'])
    months = sorted(months, key=lambda m:m['start'])
    return articles, categories, months, pages

def find_category_meta(config, path):
    meta = {}
    meta['collection_type'] = 'category'
    meta['name'] = path
    meta['display_name'] = config['category_display_names'][path] if path in config['category_display_names'] else os.path.basename(path)
    meta['active_menu_item'] = 'BLOG_ARCHIVES'

    index_path = '/'.join(['archives', path.replace('/', '_') + '.html'])
    meta['path'] = index_path
    meta['link'] = '/'.join([config['url'], index_path])
    return meta

def find_article_meta(config, path):
    meta = {}

    meta['name'] = path
    article_html = markdown2.markdown(open(path, 'r').read())
    meta['content'] = article_html
    title_finder = HTMLTitleFinder(article_html)
    meta['title'] = title_finder.headline
    meta['description'] = title_finder.first_paragraph
    meta['active_menu_item'] = 'BLOG_HOME'
    meta['changes'] = find_dates(path)

    article_path = os.path.splitext(path)[0] + '.html'
    meta['path'] = article_path
    meta['link'] = '/'.join([config['url'], article_path])
    return meta

def find_page_meta(config, path):
    meta = {}

    meta['name'] = path
    page_html = markdown2.markdown(open(path, 'r').read())
    meta['content'] = page_html
    meta['active_menu_item'] = path
    meta['changes'] = find_dates(path)

    page_path = os.path.splitext(os.path.basename(path))[0] + '.html'
    meta['path'] = page_path
    meta['link'] = '/'.join([config['url'], page_path])
    return meta

#################################################
## translate templated markdown code into html ##
#################################################

def generate_html(config, output_dir):
    articles, categories, months, pages = index_blog_structure(config)
    
    file_loader = FileSystemLoader(os.path.join('themes', config['theme'], 'templates'))
    env = Environment(loader=file_loader)
    env.globals = get_globals(config, articles, categories, months, pages)

    clear_dir(output_dir)
    generate_home(config, output_dir, env)
    generate_archives_index(config, output_dir, env)

    for category in categories:
        generate_category_collection(config, output_dir, env, category) 

    for month in months:
        generate_month_collection(config, output_dir, env, month)
    
    for article in articles:
        generate_article(config, output_dir, env, article)

    for page in pages:
        generate_page(config, output_dir, env, page)
    
    copy_assets(config, output_dir)

def generate_home(config, output_dir, environment):
    template = environment.get_template('home.template.html')
    this = {}
    this['active_menu_item'] = 'BLOG_HOME'
    html = template.render(this=this)

    export_path = os.path.join(output_dir, 'index.html')
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(html)

def generate_archives_index(config, output_dir, environment):
    template = environment.get_template('archives.template.html')
    this = {}
    this['active_menu_item'] = 'BLOG_ARCHIVES'
    html = template.render(this=this)

    export_path = os.path.join(output_dir, 'archives', 'index.html')
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(html)

def generate_category_collection(config, output_dir, environment, category):
    template = environment.get_template('collection.template.html')
    html = template.render(this=category)

    export_path = os.path.join(output_dir, category['path'])
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(html)

def generate_month_collection(config, output_dir, environment, month):
    template = environment.get_template('collection.template.html')
    html = template.render(this=month)

    export_path = os.path.join(output_dir, month['path'])
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(html)

def generate_article(config, output_dir, environment, article):
    template = environment.get_template('article.template.html')
    first_pass = template.render(this=article)
    second_pass = environment.from_string(first_pass).render()

    export_path = os.path.join(output_dir, article['path'])
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(second_pass)

def generate_page(config, output_dir, environment, page):
    template = environment.get_template('page.template.html')
    first_pass = template.render(this=page)
    second_pass = environment.from_string(first_pass).render()

    export_path = os.path.join(output_dir, page['path'])
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w') as f:
        f.write(second_pass)

def copy_assets(config, output_dir):
    export_path = os.path.join(output_dir, 'assets')
    os.makedirs(export_path, exist_ok=False)
    
    if os.path.exists(export_path):
        shutil.rmtree(export_path)

    shutil.copytree('assets', export_path, dirs_exist_ok=True)
    shutil.copytree(os.path.join('themes', config['theme'], 'assets'), export_path, dirs_exist_ok=True)
