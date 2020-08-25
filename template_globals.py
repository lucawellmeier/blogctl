import os

def get_globals(config, articles, categories, pages):
    g = {}
    g['blog_title'] = config['blog_title']
    g['home_link'] = '/'.join([config['url'], 'index.html'])
    g['articles'] = articles
    g['categories'] = categories
    g['pages'] = pages
    g['assets'] = '/'.join([config['url'], 'assets'])

    menu_items = [] 
    for i in range(len(config['menu_items'])):
        item = {}
        item['title'] = config['menu_items'][i]['title']
        item['page'] = config['menu_items'][i]['page']
        if config['menu_items'][i]['page'] == 'BLOG_HOME':
            item['link'] = g['home_link']
        else:
            item['link'] = find_page(config['menu_items'][i]['page'], pages)['link']
        menu_items.append(item)
    g['menu_items'] = menu_items

    g['find_category'] = lambda name : find_category(name, categories)
    g['category_of'] = lambda article : category_of(article, categories)
    g['parent_tree_of'] = lambda obj : parent_tree_of(obj, categories)
    g['children_of'] = lambda cat : children_of(cat, categories)
    g['find_articles_in'] = lambda cat : find_articles_in(cat, config, articles)
    g['find_article'] = lambda name : find_article(name, articles)
    g['find_page'] = lambda name : find_page(name, pages)

    return g

def find_category(name, _cats):
    return next(cat for cat in _cats if cat['name'] == name)

def category_of(article, _cats):
    return find_category(os.path.dirname(article['path']), _cats)

def parent_tree_of(obj, _cats):
    parent_strings = []
    if 'name' in obj: # category
        parent_strings = obj['name'].split('/')[:-1]
    else: # article
        parent_strings = os.path.dirname(obj['path']).split('/')
    
    parent_cats = []
    for i in range(len(parent_strings)):
        cat_name = '/'.join(parent_strings[:i+1])
        parent_cats.append(find_category(cat_name, _cats))

    if len(parent_cats) > 1:
        del parent_cats[0]

    return parent_cats

def children_of(cat, _cats):
    return [other for other in _cats 
            if other['name'].startswith(cat['name']) 
            and len(other['name'].split('/')) > len(cat['name'].split('/'))]

def find_articles_in(cat, _conf, _arts):
    return [art for art in _arts if os.path.dirname(art['name']) == cat['name']]

def find_article(name, _arts):
    return next(art for art in _arts if art['name'] == name)

def find_page(name, _pages):
    return next(page for page in _pages if page['name'] == name)
