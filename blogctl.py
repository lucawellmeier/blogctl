#!/usr/bin/python

import sys
import argparse

from utils import CustomError
from init_cmd import InitCommand
from preview_cmd import PreviewCommand

class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(prog='blogctl', 
                epilog='use "blogctl <command> -h" for details on a specific command')
        parser.add_argument('command', 
                help='available commands: init, status, save, preview, publish')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            raise CustomError('unknown command "' + args.command + '"')
        getattr(self, args.command)(sys.argv[2:])

    def init(self, args):
        parser = argparse.ArgumentParser(prog='blogctl init', 
                description='initialize new blog with dummy files')
        parser.add_argument('remote', 
                help='link to your remote GitHub Pages repo')
        initArgs = parser.parse_args(args)
        InitCommand(initArgs.remote)

    def save(self, args):
        parser = argparse.ArgumentParser(prog='blogctl save', 
                description='save changes to be published later')
        parser.parse_args(args)

    def preview(self, args):
        parser = argparse.ArgumentParser(prog='blogctl preview', 
                description='generate a preview of the current state')
        parser.parse_args(args)
        PreviewCommand()

    def publish(self, args):
        parser = argparse.ArgumentParser(prog='blogctl publish', 
                description='publish current state to the web')
        parser.parse_args(args)

    def status(self, args):
        parser = argparse.ArgumentParser(prog='blogctl status', 
                description='list unsaved and unpublished files')
        parser.parse_args(args)

if __name__ == '__main__':
    try:
        CLI()
    except CustomError as e:
        print('error: ' + e.message)
