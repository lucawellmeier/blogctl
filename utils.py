import os
import shutil
import subprocess

class CustomError(Exception):
    def __init__(self, message):
        self.message = message

def newdir(dirname):
    os.makedirs(os.path.join(os.getcwd(), dirname), exist_ok=True)

def newfile(filename, content):
    path = os.path.join(os.getcwd(), filename)
    if os.path.isfile(path):
        raise CustomError('file ' + path + ' already exists')
    with open(path, 'w') as f:
        f.write(content)

def cleardir(directory):
    for filename in os.listdir(directory):
        if filename.startswith('.'):
            continue
        path = os.path.join(directory, filename)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def flatten(directory):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path) or os.path.islink(path):
            shutil.move(path, os.path.join(os.getcwd(), filename))
        elif os.path.isdir(path):
            shutil.move(path, os.getcwd())
    shutil.rmtree(directory)

def git(args):
    process = subprocess.Popen(['git'] + args, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if 'fatal' in err.decode():
        raise CustomError('calling git command "' + ' '.join(args) + '":\n' + err.decode())
    return out.decode()

def dt_smart_formatter(dt):
    return dt.strftime('%c')
