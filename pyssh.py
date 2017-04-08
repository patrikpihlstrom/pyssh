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
    if any(host in line for line in open(path.dirname(__file__)+'/blacklist').readlines()):
        return True

    return False

def blacklist_host(host):
    if not get_host_blacklisted:
        with open(path.dirname(__file__)+'/blacklist', 'a') as blacklist:
            blacklist.write(arguments['Host']+'\n')

def should_update_host_config():
    return False # TODO remove
    if get_host_blacklisted(arguments['Host']):
        return False

    question = 'Update host config? [y/n/N(Don\'t ask again for this host)]: '
    answer = ''
    if len(key) > 0:
        if 'IdentityFile' not in config or key != config['IdentityFile'] or 'User' in arguments is not 'User' in config:
            print(question, end='')
            answer = raw_input()

    if answer in ['y', 'Y']:
        return True
    elif answer == 'N':
        blacklist_host(arguments['Host'])

    return False

def update_host_config():
    found_host = False

    return False # TODO fix
    with open(path.expanduser('~/.ssh/config'), 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        for line in lines:
            if 'Host ' in line:
                if found_host:
                    file.close()
                    return True
                elif 'Host ' + arguments['Host'] in line:
                    found_host = True

            if found_host:
                lineArgs = filter(None, line.split(' '))
                if len(lineArgs) >= 2 and lineArgs[1] is not lineArgs[0] in arguments:
                    line = line.replace(lineArgs[1], arguments[lineArgs[0]]).rstrip()
                    print(line.rstrip())

            file.write(line)

def new_host_config():
    if get_host_blacklisted(arguments['Host']):
        return False

    print('Create host config? [y/n/N(Don\'t ask again for this host)]: ', end='')
    answer = raw_input()

    if answer == 'N':
        blacklist_host(arguments['Host'])
        return False
    elif answer not in ['y', 'Y']:
        return False

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
        file.write('Host '+arguments['Host']+'\n')
        for arg in arguments.keys():
            if (arg != 'Host'):
                file.write('    '+arg+' '+arguments[arg]+'\n')

user = get_user(args)
host = get_host(args)
key = get_arg(args, ['-i'])
port = get_arg(args, ['-P', '-p'], '22')

if not path.isfile(path.expanduser('~/.ssh/config')):
        open(path.expanduser('~/.ssh/config'), 'a').close()

config = get_host_config(host, open(path.expanduser('~/.ssh/config')))
arguments = {}

arguments['ForwardAgent'] = 'Yes'
arguments['IdentityFile'] = key

if port != '22':
    arguments['Port'] = port

arguments['User'] = user

if len(host) > 0:
    arguments['Host'] = host
else:
    arguments['Host'] = args[1]

if not config:
    new_host_config()
elif should_update_host_config():
    update_host_config()

ssh = args
ssh[0] = 'ssh'
call(ssh)

