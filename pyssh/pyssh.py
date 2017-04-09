#!/usr/bin/python

from __future__ import print_function
import sys
import fileinput
import re
from os import path
import argparse


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

def get_arg(arguments, inputs, defaultNo = False, defaultYes = True):
    for _input in inputs:
        if _input in arguments: # TODO: make work with both -ikey.rsa & -i key.rsa
            try:
                if arguments[arguments.index(_input) + 1][0] == _input:
                    print(_input+':'+str(defaultYes))
                    return defaultYes
                elif arguments[arguments.index(arg) + 1][0] != '-':
                    print(_input+':'+str(arguments[arguments.index(arg) + 1]))
                    return arguments[arguments.index(arg) + 1]
            except Exception:
                pass

    print(str(inputs)+':'+str(defaultNo))
    return defaultNo

class Pyssh:
    options = {}
    config_path = ''
    argv = ''
    args = {
            'IdentityFile': {'args': ['-i'], 'defaultNo': False, 'defaultYes': True},
            'Port': {'args': ['-P', '-p-'], 'defaultNo': '22', 'defaultYes': True},
            'ForwardAgent': {'args': ['-A'], 'defaultNo': 'No', 'defaultYes': 'Yes'},
            'save': {'args': ['--save'], 'defaultNo': False, 'defaultYes': True}
            }

    def __init__(self, argv, test = False):
        self.argv = argv
        self.test = test

        self.options['User'] = get_user(argv)
        self.options['Host'] = get_host(argv)


        parser = argparse.ArgumentParser()
        for arg, vals in self.args.iteritems():
            parser.add_argument(vals['args'], default=vals['defaultNo'])

        args = parser.parse_args()
        print(args.IdentityFile)

        for arg, val in self.args.iteritems():
            self.options[arg] = get_arg(argv, val['args'], val['defaultNo'], val['defaultYes'])

        if self.test:
            self.config_path = path.dirname(__file__)+'/config'
        else:
            self.config_path = path.expanduser('~/.ssh/config')

        if type(self.options['IdentityFile']) is str:
            self.options['IdentityFile'] = path.realpath(self.options['IdentityFile'])

        print(self.options)
        if not path.isfile(self.config_path):
            open(self.config_path, 'a').close()

    def get_host_config(self):
        config = open(self.config_path)
        lines = [line.strip() for line in config.readlines()]
        found_host = False
        host_config = {}

        for line in lines:
            if 'Host ' in line:
                if found_host:
                    return host_config
                elif line.rsplit(None, 1)[-1] == self.options['Host']:
                    host_config['Host'] = self.options['Host']
                    found_host = True
            elif found_host:
                conf = line.split(" ")
                if len(conf) >= 2:
                    host_config[conf[0]] = conf[1]

        if not found_host:
            return False

        return host_config

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

