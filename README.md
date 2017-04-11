# PYSSH #
[![Build Status](https://travis-ci.org/patrikpihlstrom/pyssh.svg?branch=master)](https://travis-ci.org/patrikpihlstrom/pyssh)


### Features ###

This script will scan your ssh config for the given host. 
If the host wasn't found, you'll be asked if you would like to save the host and all of the arguments in your config.


### Usage ###

I recommend creating an alias `alias ssh='python /path/to/pyssh.py'`

In order to save a host config, simply use the `--save` argument when invoking the ssh command.
If the host isn't in your ~/.ssh/config file, you'll be asked if you want to add the host, as well as prompted for each of the arguments that you specified.
Each argument's value will default to the value you initially specified.

#### Example ####
```
$ ssh user@example -i key.rsa -p 123 -A --save
User[user]:
Port[123]:
IdentityFile[key.rsa]:
HostName(ip/dns)[example]:
Host(alias)[example]:
ForwardAgent[Yes]:
```
*~/.ssh/config*
```
Host example
    IdentityFile ~/key.rsa
    HostName example
    User user
    ForwardAgent Yes
    Port 123
```
*You should propably store a backup of your ssh config in case of nasty bugs...*

