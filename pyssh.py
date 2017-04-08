#!/usr/bin/python

from __future__ import print_function
import sys
import fileinput
from os import path
from subprocess import call


args = sys.argv

if len(args) < 2:
    sys.exit()

def get_user(args):
    user_host = args[1].split("@")
    if len(user_host) == 2:
        return user_host[0]

    return ''

def get_host(args):
    user_host = args[1].split("@")
    if len(user_host) == 2:
        return user_host[1]

    return ''

def get_arg(arguments, args, default = ''):
    for arg in args:
        if arg in arguments:
            try:
                return arguments[arguments.index(arg) + 1]
            except Exception:
                pass

    return default

def get_host_config(host, config):
    lines = [line.strip() for line in config.readlines()]
    found_host = False
    host_config = {}

    for line in lines:
        if 'Host ' in line:
            if found_host:
                return host_config
            elif 'Host ' + host in line:
                host_config['Host'] = host
                found_host = True
        elif found_host:
            conf = line.split(" ")
            if len(conf) >= 2:
                host_config[conf[0]] = conf[1]

    if not found_host:
        return False

    return host_config

def get_host_blacklisted(host):
    if any(host in line for line in open(path.expanduser('~/.pyssh')).readlines()):
        return True

    return False

def should_update_host_config(key):
    if get_host_blacklisted(arguments['Host']):
        return False

    question = 'Update host config? [y/n/N(Don\'t ask again for this host)]: '
    answer = ''
    if len(key) > 0:
        if 'IdentityFile' not in config or key != config['IdentityFile']:
            print(question, end='')
            answer = raw_input()

    if answer == '':
        if 'User' in arguments != config['User']:
            print(question, end='')
            answer = raw_input()

    if answer in ['y', 'Y']:
        return True
    elif answer == 'N':
        with open(path.expanduser('~/.pyssh'), 'a') as blacklist:
            blacklist.write(arguments['Host']+'\n')

    return False

def update_host_config():
    found_host = False

    for line in fileinput.input(path.expanduser('~/.ssh/config'), inplace=True):
        if 'Host ' in line:
            if found_host:
                return True
            elif 'Host ' + arguments['Host'] in line:
                found_host = True
        elif found_host:
            print(line)
            conf = line.split(' ')
            if len(conf) >= 2 and conf[0] in arguments:
                conf[1] = arguments[conf[0]]
                line = ' '.join(conf)

def new_host_config():
    if get_host_blacklisted(arguments['Host']):
        return False

    print('Create host config? [y/n/N(Don\'t ask again for this host)]: ', end='')
    answer = raw_input()

    if answer not in ['y', 'Y']:
        return False
    elif answer == 'N':
        with open(path.expanduser('~/.pyssh'), 'a') as blacklist:
            blacklist.write(arguments['Host']+'\n')

    arguments['HostName'] = arguments['Host']
    for arg in sorted(arguments.keys(), reverse=True):
        if arg == 'Host':
            arguments[arg] = raw_input(arg+'(alias)['+arguments[arg]+']:') or arguments[arg]
        elif arg == 'HostName':
            arguments[arg] = raw_input(arg+'(ip/dns)['+arguments[arg]+']:') or arguments[arg]
        else:
            arguments[arg] = raw_input(arg+'['+arguments[arg]+']:') or arguments[arg]

    with open(path.expanduser('~/.ssh/config'), 'a') as file:
        file.write('\n')
        file.write(arg+' '+arguments['Host']+'\n')
        for arg in arguments.keys():
            if (arg != 'Host'):
                file.write('    '+arg+' '+arguments[arg]+'\n')

user = get_user(args)
host = get_host(args)
key = get_arg(args, ['-i'])
port = get_arg(args, ['-P', '-p'], '22')
forward_agent = get_arg(args, ['-A'])
config = get_host_config(host, open(path.expanduser('~/.ssh/config')))
arguments = {}

if len(user) > 0:
    arguments['User'] = user

if len(host) > 0:
    arguments['Host'] = host
else:
    arguments['Host'] = args[1]

if len(key) > 0:
    arguments['IdentityFile'] = key

if port != '22':
    arguments['Port'] = port

if forward_agent:
    arguments['ForwardAgent'] = 'Yes'

if not config and path.isfile(path.expanduser('~/.ssh/config')):# and len(key) > 0:
    new_host_config()
elif should_update_host_config(key):
    update_host_config()

ssh = args
ssh[0] = 'ssh'
call(ssh)

