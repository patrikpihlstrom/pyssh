#!/usr/bin/python

import sys
from os import path
import unittest
import shlex
import json
import ruamel.yaml as yaml

sys.path.append(path.dirname(path.abspath(__file__))+'/../')
from pyssh import pyssh

user = ''
host = ''
case = ''

class TestPyssh(unittest.TestCase):
    def __init__(self, function, command):
        super(TestPyssh, self).__init__(function)
        self.pyssh = pyssh.Pyssh(shlex.split(command), True)

    def test_get_user(self):
        self.assertEqual(pyssh.get_user(self.pyssh.argv), 'user')

    def test_get_host(self):
        self.assertEqual(pyssh.get_host(self.pyssh.argv), 'example.host')

    def test_get_arg(self):
        args = self.pyssh.args
        argv = self.pyssh.argv

        for key, val in case.iteritems():
            if key != 'commands':
                self.assertEqual(val if type(val) == bool else str(val), pyssh.get_arg(argv, args[key]['args'], args[key]['defaultNo'], args[key]['defaultYes']))

    def test_get_host_config(self):
        self.assertTrue(True)

    def test_get_host_blacklisted(self):
        self.assertTrue(True)

    def test_blacklist_host(self):
        self.assertTrue(True)

    def test_new_host_config(self):
        self.assertTrue(True)

if __name__ == '__main__':
    with open(path.dirname(path.abspath(__file__))+'/'+'cases.json') as file:
        json = json.load(file)
        cases = json['cases']
        user = json['user']
        host = json['host']

        for _case in cases:
            case = _case
            suite = unittest.TestSuite()
            for command in _case['commands']:
                print(command)
                suite.addTest(TestPyssh('test_get_user', command))
                suite.addTest(TestPyssh('test_get_host', command))
                suite.addTest(TestPyssh('test_get_arg', command))
                #suite.addTest(TestPyssh('test_get_host_config', command))
                #suite.addTest(TestPyssh('test_get_host_blacklisted', command))
                #suite.addTest(TestPyssh('test_blacklist_host', command))
                #suite.addTest(TestPyssh('test_new_host_config', command))

            unittest.TextTestRunner().run(suite)

