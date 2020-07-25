from utils import git

class CloneCommand:
    def __init__(self, remote):
        git(['clone', remote, '.'])
        git(['checkout', 'dev'])

