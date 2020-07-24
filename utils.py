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
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def git(args):
    process = subprocess.Popen(['git'] + args, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if 'fatal' in err.decode():
        raise CustomError('(from git) ' + err.decode())
    return out.decode()

def dt_smart_formatter(dt):
    return dt.strftime('%c')
