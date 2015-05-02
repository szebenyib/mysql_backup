#!/usr/bin/env python
# Source: http://codepoets.co.uk/2010/python-script-to-backup-mysql-databases-on-debian/
import os
import time
import ConfigParser
import unittest

class Backup():
    def __init__(self,
                 configpath):
        """Creates a Backup instance with the configpath that holds the
        credentials to access mysql. It is generally found under:
        "/etc/mysql/debian.cnf" on debian based systems including Ubuntu.
        """
        self.configpath = configpath
        self.filestamp = None
        self.login_info = None
        self.database_list = None

    def set_filestamp(self):
        """Obtains a date stamp for the files from the date.
        @return: a string YYYY-MM-DD
        """
        self.filestamp = time.strftime("%Y-%m-%d")

    def read_config(self):
        """Reads the databse config from its location.
        It sets up the login_info dictionary with "user", "password", "host".
        """
        config = ConfigParser.ConfigParser()
        try:
            os.stat(self.configpath)
        except OSError:
            raise OSError
        config.read(self.configpath)
        login_info = dict()
        login_info["username"] = config.get("client", "user")
        login_info["password"] = config.get("client", "password")
        login_info["host"] = config.get("client", "host")
        self.login_info = login_info

    def get_list_of_databases(self):
        database_list_command = ("mysql -u %s -p%s -h %s --silent -N" + \
                                 " -e 'show databases'") % (
                                 self.login_info["username"],
                                 self.login_info["password"],
                                 self.login_info["host"])
        f = os.popen(database_list_command, 'r')
        database_list = f.readlines()
        return database_list

    def get_filename_of_backup(self, path, database, filestamp):
        last_char_of_path = path[len(path) - 1]
        if last_char_of_path != "/":
            path = path + "/"
        filename = (path + "%s-%s.sql") % (database, filestamp)
        return filename

    def backup_databases(self, database_list, backuppath):
            for database in database_list:
                database = database.strip()
                if database not in ["information_schema",
                                    "performance_schema"]:
                    filename = self.get_filename_of_backup(path=backuppath,
                                                           database=database,
                                                           filestamp=self.filestamp)
                    try:
                        os.stat(backuppath)
                    except OSError:
                        print "Not writable: " + filename
                        raise OSError
                    os.popen(("mysqldump -u %s -p%s -h %s -e --opt -c %s" + \
                              " --ignore-table=mysql.event | " + \
                              "gzip -c > %s.gz") % (self.login_info["username"],
                                                    self.login_info["password"],
                                                    self.login_info["host"],
                                                    database,
                                                    filename))
