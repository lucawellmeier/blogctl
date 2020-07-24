import os
from html.parser import HTMLParser
import markdown2
from jinja2 import Environment, FileSystemLoader
from utils import CustomError

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

def findGitDatesFor(articleFile):
    return '', ''

def findArticleMeta(articleFile, config):
    articleMeta = {}

    exportFilename = os.path.splitext(os.path.basename(articleFile))[0] + '.html'
    articleMeta['export_file'] = os.path.join('articles', exportFilename)
    articleMeta['url'] = os.path.join(config['url'], articleMeta['export_file'])
    with open(articleFile, 'r') as f:
        articleMeta['content'] = markdown2.markdown(f.read())

    headlineFinder = HeadlineFinder(articleMeta['content'])
    if not headlineFinder.title:
        raise CustomError('no headline found in article ' + articleFile)
    articleMeta['title'] = headlineFinder.title

    articleMeta['published'], articleMeta['last_change'] = findGitDatesFor(articleFile)
    return articleMeta

def exportArticle(articleMeta, outputDir, config, blogInfo):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(config['article_template'])
    html = template.render(blog=blogInfo, article=articleMeta)
    
    path = os.path.join(outputDir, articleMeta['export_file'])
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, 'w') as f:
        f.write(html)

def exportHome(outputDir, config, blogInfo):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(config['home_template'])
    html = template.render(blog=blogInfo)

    path = os.path.join(outputDir, 'index.html')
    with open(path, 'w') as f:
        f.write(html)

def generate(outputDir, config):
    ls = os.listdir('articles')
    files = [os.path.join('articles', f) for f in os.listdir('articles')]
    articleFiles = [f for f in files if os.path.isfile(f) and os.path.splitext(f)[1] == '.md']
    articles = [findArticleMeta(f, config) for f in articleFiles]

    blogInfo = {}
    blogInfo['title'] = config['blog_title']
    blogInfo['url'] = config['url']
    blogInfo['articles'] = articles

    for article in articles:
        exportArticle(article, outputDir, config, blogInfo)
    exportHome(outputDir, config, blogInfo)
