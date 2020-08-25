#!/usr/bin/python

import sys
import argparse

from utils import BlogError
from commands import InitCommand, CloneCommand, SaveCommand, PreviewCommand, PublishCommand

class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(prog='octoblog', 
                epilog='use "octoblog <command> -h" for details on a specific command')
        parser.add_argument('command', 
                help='available commands: init, clone, status, save, preview, publish')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            raise BlogError('unknown command "' + args.command + '"')
        getattr(self, args.command)(sys.argv[2:])

    def init(self, args):
        parser = argparse.ArgumentParser(prog='octoblog init', 
                description='initialize new blog with dummy files')
        parser.add_argument('remote', 
                help='link to your remote GitHub Pages repo')
        initArgs = parser.parse_args(args)
        InitCommand(initArgs.remote)

    def clone(self, args):
        parser = argparse.ArgumentParser(prog='octoblog clone', 
                description='clone existing GitHub Pages octoblog repo')
        parser.add_argument('remote', 
                help='link to your repo')
        cloneArgs = parser.parse_args(args)
        CloneCommand(cloneArgs.remote)

    def save(self, args):
        parser = argparse.ArgumentParser(prog='octoblog save', 
                description='save changes to be published later')
        parser.parse_args(args)
        SaveCommand()

    def preview(self, args):
        parser = argparse.ArgumentParser(prog='octoblog preview', 
                description='generate a preview of the current state')
        parser.parse_args(args)
        PreviewCommand()

    def publish(self, args):
        parser = argparse.ArgumentParser(prog='octoblog publish', 
                description='publish current state to the web')
        parser.parse_args(args)
        PublishCommand()

    def status(self, args):
        parser = argparse.ArgumentParser(prog='octoblog status', 
                description='list unsaved and unpublished files')
        parser.parse_args(args)

if __name__ == '__main__':
    try:
        CLI()
    except BlogError as e:
        print('error: ' + e.message)
