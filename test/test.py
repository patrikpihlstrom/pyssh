#!/usr/bin/python

import sys
from os import path
from os import remove
import unittest
import shlex
import json
import shutil

sys.path.append(path.dirname(path.abspath(__file__))+'/../')
from pyssh import pyssh

user = ''
host = ''
case = ''

class TestPyssh(unittest.TestCase):
    def __init__(self, function, command):
        super(TestPyssh, self).__init__(function)
        self.pyssh = pyssh.Pyssh(shlex.split(command), True)

    @classmethod
    def setUpClass(cls):
        test_path = path.dirname(path.abspath(__file__))
        shutil.copyfile(test_path+'/dummy_config', test_path+'/config')

    @classmethod
    def tearDownClass(cls):
        test_path = path.dirname(path.abspath(__file__))
        remove(test_path+'/config')

    def test_get_user(self):
        self.assertEqual(pyssh.get_user(self.pyssh.argv), user)

    def test_get_host(self):
        self.assertEqual(pyssh.get_host(self.pyssh.argv), host)

    def test_get_arg(self):
        argv = self.pyssh.argv

        for key, val in case.iteritems():
            if key not in ['commands', 'host_in_config', 'host']:
                arg = next((a for a in self.pyssh.args if a['argument'] == key), None)
                self.assertEqual(val if type(val) == bool else str(val), pyssh.get_arg(argv, arg, user, host))

    def test_get_host_in_config(self):
        self.assertEqual(case['host_in_config'], self.pyssh.get_host_in_config(host))

if __name__ == '__main__':
    with open(path.dirname(path.abspath(__file__))+'/'+'cases.json') as file:
        json = json.load(file)
        cases = json['cases']
        user = json['user']
        host = json['host']

        for _case in cases:
            case = _case
            if 'host' in case:
                host = case['host']

            suite = unittest.TestSuite()
            for command in _case['commands']:
                suite.addTest(TestPyssh('test_get_user', command))
                suite.addTest(TestPyssh('test_get_host', command))
                suite.addTest(TestPyssh('test_get_arg', command))
                suite.addTest(TestPyssh('test_get_host_in_config', command))

            unittest.TextTestRunner().run(suite)

