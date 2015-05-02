mysql\_backup
=============

A python script to backup mysql databases.

I use this script to backup the databases on my homeserver. It
reads what databases there are on the server and saves them via
mysql dumps to gz files in a given directory.

Usage
=====

Backup
------

To backup your mysql files you are expected to provide the script two
paths. The config path holds the login credentials which are by
default at /etc/mysql/debian.cnf on debian based systems. The backup path
specifies where you want to see your backups.

Sample usage:
    python mysql_backup.py

*Note: you may need to run it with sudo.*

Unittests
---------

To run the tests after having checked the setup section:
    python -m unittest discover

Alternatively rerun the tests on every modification
(install it via pip install rerun first):
    rerun "python -m unittest discover"

Setup
-----

The script relies on two paths: the configpath that holds
the credentials to access mysql. And the backuppath refers to the
folder where you want to store your backups. These can be configured
in the config.txt that must reside in the same place where the script
is stored.


Credits
=======

Credits go to David Goodwin, I have found his little script here:

http://codepoets.co.uk/2010/python-script-to-backup-mysql-databases-on-debian/

My script is relying heavily on the solutions that David has come up with.
