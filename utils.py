import os
import shutil
import subprocess
import re
from datetime import datetime
from html.parser import HTMLParser

################################
## error handling and logging ##
################################

class BlogError(Exception):
    def __init__(self, message):
        self.message = message

###########################
## file system utilities ##
###########################

# creates a new directory if it not exists
def new_dir(dirname):
    os.makedirs(os.path.join(os.getcwd(), dirname), exist_ok=True)

# creates a new file but throws BlogError if it already exists
def new_file(filename, content):
    path = os.path.join(os.getcwd(), filename)
    if os.path.isfile(path):
        raise BlogError('file ' + path + ' already exists')
    with open(path, 'w') as f:
        f.write(content)

# removes all files and subdirectories in given directory ignoring dotfiles
def clear_dir(directory):
    for filename in os.listdir(directory):
        if filename.startswith('.'):
            continue
        path = os.path.join(directory, filename)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

# moves all files and dirs from given directory to cwd
def flatten(directory):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path) or os.path.islink(path):
            shutil.move(path, os.path.join(os.getcwd(), filename))
        elif os.path.isdir(path):
            shutil.move(path, os.getcwd())
    shutil.rmtree(directory)

#################
## git helpers ##
#################

# starts given git command. throws stderr through BlogError and returns stdout
def git(args):
    process = subprocess.Popen(['git'] + args, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if 'fatal' in err.decode():
        raise BlogError('calling git command "' + ' '.join(args) + '":\n' + err.decode())
    return out.decode()

# follows the commit history of a given file (date and commit message)
def find_all_commits_for(article_file):
    log = git(['log', '--follow', '--', article_file])
    lines = log.splitlines(keepends=True)

    raw_commits = []
    for line in lines:
        if re.match('^commit', line):
            raw_commits.append([line])
        elif len(raw_commits) > 0:
            raw_commits[-1] += [line]
    
    commits = []
    for raw_commit in raw_commits:
        date_line = raw_commit[2] # line which contains the commit date
        date_string = re.match(r'^\s*Date:\s*(.+)\s*$', date_line).group(1)
        
        commits.append({
            'date': datetime.strptime(date_string, '%c %z'),
            'message': raw_commit[4].lstrip().rstrip(), })

    return sorted(commits, key=lambda commit: commit['date'])

#####################
## markdown helper ##
#####################

# finds the first headline and the first paragraph underneath
class HTMLTitleFinder(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.headline = ''
        self.first_paragraph = ''
        self._found_first_headline = False
        self._in_first_headline = False
        self._headline_tag = None
        self._found_first_paragraph = False
        self._in_first_paragraph = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if not self._found_first_headline:
            if re.match(r'h[123456]{1}', tag):
                self._found_first_headline = True
                self._in_first_headline = True
                self._headline_tag = tag
        elif self._found_first_headline and not self._in_first_headline and not self._found_first_paragraph:
            if tag == 'p':
                self._found_first_paragraph = True
                self._in_first_paragraph = True

    def handle_endtag(self, tag):
        if self._in_first_headline:
            if tag == self._headline_tag:
                self._in_first_headline = False
        elif self._in_first_paragraph:
            if tag == 'p':
                self._in_first_paragraph = False

    def handle_data(self, data):
        if self._in_first_headline:
            self.headline = data
        elif self._in_first_paragraph:
            self.first_paragraph = data
