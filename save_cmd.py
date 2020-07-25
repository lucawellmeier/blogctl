from utils import git

class SaveCommand:
    def __init__(self):
        print('---> saving to github')
        git(['pull', '--allow-unrelated-history', 'origin', 'dev'])
        git(['add', '.'])
        git(['commit', '-m', 'blogctl save'])
        git(['push', 'origin', 'dev'])
        print('---> done')
