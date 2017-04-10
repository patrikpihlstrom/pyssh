#!/usr/bin/python

from __future__ import print_function
import sys
import fileinput
import re
from os import path
import os
from optparse import OptionParser


def get_user(args):
    try:
        user_host = str(args).split("@")
        if len(user_host) == 2:
            return re.findall(r"[\w]+", user_host[0])[-1]
    except Exception:
        return ''

    return ''

def get_host(args):
    try:
        user_host = str(args).split("@")
        if len(user_host) == 2:
            host = user_host[1].split(' ')[0].translate(None, '\'],')
            if len(host)  > 0:
                return host

            return args[1]
    except Exception:
        return args[1]

    return args[1]

def get_arg(argv, arg, user, host):
    for _arg in argv:
        if _arg not in [user, host]:
            for __arg in arg['args']:
                if _arg.startswith(__arg):
                    if _arg == __arg:
                        try:
                            next_arg = argv[argv.index(_arg) + 1]
                            if next_arg[0] != '-' and '@' not in next_arg:
                                return next_arg
                            else:
                                return arg['defaultYes']
                        except Exception:
                                return arg['defaultYes']

                    else:
                        return _arg[len(__arg):]

    return arg['defaultNo']

class Pyssh:
    options = {}
    config_path = ''
    argv = ''
    args = [
            {'argument': 'IdentityFile', 'args': ['-i'], 'defaultNo': False, 'defaultYes': True},
            {'argument': 'Port', 'args': ['-p', '-P'], 'defaultNo': '22', 'defaultYes': True},
            {'argument': 'ForwardAgent', 'args': ['-A'], 'defaultNo': 'No', 'defaultYes': 'Yes'},
            {'argument': 'save', 'args': ['--save'], 'defaultNo': False, 'defaultYes': True}
            ]

    def __init__(self, argv, test = False):
        self.argv = argv
        self.test = test

        self.options['User'] = get_user(argv)
        self.options['Host'] = get_host(argv)

        for arg in self.args:
            self.options[arg['argument']] = get_arg(argv, arg, self.options['User'], self.options['Host'])

        if self.test:
            self.config_path = os.getcwd()+'/config'
        else:
            self.config_path = path.expanduser('~/.ssh/config')

        if type(self.options['IdentityFile']) is str:
            self.options['IdentityFile'] = path.realpath(self.options['IdentityFile'])

        if not path.isfile(self.config_path):
            open(self.config_path, 'a').close()

    def get_host_in_config(self, host = ''):
        if host == '':
            host = self.options['Host']

        config = open(self.config_path)
        lines = [line.strip() for line in config.readlines()]

        for line in lines:
            if 'Host ' in line:
                if line.rsplit(None, 1)[-1] == host:
                    return True

        return False

    def new_host_config(self):
        # get options
        self.options['HostName'] = self.options['Host']
        for arg in sorted(self.options.keys(), reverse=True):
            if arg == 'Host':
                self.options[arg] = raw_input(arg+'(alias)['+self.options[arg]+']:') or self.options[arg]
            elif arg == 'HostName':
                self.options[arg] = raw_input(arg+'(ip/dns)['+self.options[arg]+']:') or self.options[arg]
            elif arg != 'save':
                self.options[arg] = raw_input(arg+'['+(self.options[arg] if type(self.options[arg]) is str else '')+']:') or self.options[arg]

        # write options
        with open(self.config_path, 'a') as file:
            file.write('\n')
            file.write('Host '+self.options['Host']+'\n')
            for arg in self.options.keys():
                if arg != 'Host' and self.options[arg] != False:
                    file.write('    '+arg+' '+self.options[arg]+'\n')

