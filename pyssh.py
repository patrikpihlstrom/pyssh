#!/usr/bin/python

from __future__ import print_function
import sys
import fileinput
import re
from os import path
from subprocess import call


args = sys.argv

if len(args) < 2:
    sys.exit()

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
            return re.findall(r"[\w]+", user_host[1])[0]
    except Exception:
        return args[1]

    return args[1]

def get_arg(arguments, args, default = ''):
    for arg in args:
        if arg in arguments:
            try:
                return arguments[arguments.index(arg) + 1]
            except Exception:
                return arg
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
            elif line.rsplit(None, 1)[-1] == host:
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

def new_host_config():
    if get_host_blacklisted(arguments['Host']):
        return False

    print('Create host config? [y/n/N(Don\'t ask again for this host)][y]: ', end='')
    answer = raw_input()

    if answer == 'N':
        blacklist_host(arguments['Host'])
        return False
    elif answer != '' and answer not in ['y', 'Y']:
        return False

    arguments['HostName'] = arguments['Host']
    for arg in sorted(arguments.keys(), reverse=True):
        if arg == 'Host':
            arguments[arg] = raw_input(arg+'(alias)['+arguments[arg]+']:') or arguments[arg]
        elif arg == 'HostName':
            arguments[arg] = raw_input(arg+'(ip/dns)['+arguments[arg]+']:') or arguments[arg]
        elif len(arguments[arg]) > 0:
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

arguments['ForwardAgent'] = 'Yes' if '-A' == get_arg(args, ['-A']) else 'No'
arguments['Port'] = port
arguments['User'] = user

if len(host) > 0:
    arguments['Host'] = host
else:
    arguments['Host'] = args[1]

if len(key) > 0:
    arguments['IdentityFile'] = path.realpath(key)

if not config:
    new_host_config()

ssh = args
ssh[0] = 'ssh'
call(ssh)

