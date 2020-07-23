import os
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

def git(args):
    process = subprocess.Popen(['git'] + args, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out, err
