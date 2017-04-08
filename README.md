# PYSSH #

Save ssh host configs


### Features ###

This script will scan your ssh config for the given host. 
If the host wasn't found, you'll be asked if you would like to save the host and all of the parameters in your config.

If the host was found, but some of the parameters differ, you'll be asked if you want to update the config.


### Usage ###

I recommend creating an alias
	`alias ssh='python /path/to/pyssh.py'`

In order to save a host confi, just execute the ssh command as per usual.
If the host isn't present in your ~/.ssh/config file, you'll be asked if you want to save the host to your config file.
You will also be prompted for each of the arguments that you specified.
What this means is, all you have to do is hit enter until you're either asked for authentication, or you've successfully logged in.

#### Example ####
```
$ ssh user@example -i key.rsa -p 123 -A
Create host config? [y/n/N(Don't ask again for this host)][y]: 
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

I recommend storing a backup of your ssh config in case of nasty bugs.

