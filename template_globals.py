import os

def get_globals(config, articles, categories):
    g = {}
    g['blog_title'] = config['blog_title']
    g['articles'] = articles
    g['categories'] = categories

    g['find_category'] = lambda name : find_category(name, categories)
    g['category_of'] = lambda article : category_of(article, categories)
    g['parent_tree_of'] = lambda obj : parent_tree_of(obj, categories)
    g['children_of'] = lambda cat : children_of(cat, categories)
    g['find_articles_in'] = lambda cat : find_articles_in(cat, articles)
    g['get_asset'] = lambda asset_file : get_asset(asset_file, config)

    return g

def find_category(name, _cats):
    return next(cat for cat in _cats if cat['name'] == name)

def category_of(article, _cats):
    return find_category(os.path.dirname(article['link']), _cats)

def parent_tree_of(obj, _cats):
    parent_strings = []
    if 'name' in obj: # category
        parent_strings = obj['name'].split('/')[:-1]
    else: # article
        parent_strings = os.path.dirname(obj['link']).split('/')
    
    parent_cats = []
    for i in range(len(parent_strings)):
        cat_name = '/'.join(parent_strings[:i+1])
        parent_cats.append(find_category(cat_name, _cats))
    return parent_cats

def children_of(cat, _cats):
    return [other for other in _cats 
            if other['name'].startswith(cat['name']) 
            and len(other['name'].split('/')) > len(cat['name'].split('/'))]

def find_articles_in(cat, _arts):
    return [art for art in _arts if os.path.dirname(art['link']) == cat['name']]

def get_asset(asset_file, _config):
    return '/'.join([_config['url'], 'assets', asset_file])
