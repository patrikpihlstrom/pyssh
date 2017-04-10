#!/usr/bin/python

import sys
import os
from subprocess import call

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pyssh import pyssh


if any('--save' == x for x in sys.argv):
    pyssh = pyssh.Pyssh(sys.argv)

    config = pyssh.get_host_in_config()
    if not config:
        pyssh.new_host_config()

    sys.argv.remove('--save')

ssh = sys.argv
ssh[0] = 'ssh'
call(ssh)
