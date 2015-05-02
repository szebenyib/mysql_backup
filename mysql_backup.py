#!/usr/bin/env python
# Source: http://codepoets.co.uk/2010/python-script-to-backup-mysql-databases-on-debian/
import os
import time
import ConfigParser
import unittest

class Backup():
    def __init__(self,
                 configpath,
                 backuppath):
        """Creates a Backup instance with the configpath that holds the
        credentials to access mysql. It is generally found under:
        "/etc/mysql/debian.cnf" on debian based systems including Ubuntu.
        A backuppath is also required that specifies where the backup files
        will be stored.
        """
        self.configpath = configpath
        self.check_path(self.configpath)
        self.backuppath = self.correct_path(backuppath)
        self.check_path(self.backuppath)
        self.filestamp = time.strftime("%Y-%m-%d")
        self.login_info = None
        self.database_list = None

    def check_path(self, path):
        """Checks if the path is accessible to the script.
        @param path: the path to check
        @raises OSError if the path is not accessible
        """
        try:
            os.stat(path)
        except OSError:
            print("Path is not accessible for the script: " + path)
            raise OSError

    def correct_path(self, path):
        """It adds trailing slashes if they are not present.
        @param path: the path to check
        """
        last_char_of_path = path[len(path) - 1]
        if last_char_of_path != "/":
            path = path + "/"
        else:
            path = path
        return path

    def read_config(self):
        """Reads the databse config from its location.
        It sets up the login_info dictionary with "user", "password", "host".
        """
        config = ConfigParser.ConfigParser()
        config.read(self.configpath)
        login_info = dict()
        login_info["username"] = config.get("client", "user")
        login_info["password"] = config.get("client", "password")
        login_info["host"] = config.get("client", "host")
        self.login_info = login_info

    def read_list_of_databases(self):
        """Reads the list of databases via executing a mysql command and
        fills the database list of the class.
        """
        database_list_command = ("mysql -u %s -p%s -h %s --silent -N" + \
                                 " -e 'show databases'") % (
                                 self.login_info["username"],
                                 self.login_info["password"],
                                 self.login_info["host"])
        f = os.popen(database_list_command, 'r')
        database_list = f.readlines()
        self.database_list = database_list

    def get_filename_of_backup(self, database):
        """Creates the filename for the given database to backup.
        @return: the filename as string
        """
        filename = (self.backuppath + "%s-%s.sql") % (database, self.filestamp)
        return filename

    def backup_databases(self):
        """Actually performs the database backup by dumping them from mysql
        and writing them to a file at the same time.
        """
        for database in self.database_list:
            database = database.strip()
            if database not in ["information_schema",
                                "performance_schema"]:
                filename = self.get_filename_of_backup(database=database)
                os.popen(("mysqldump -u %s -p%s -h %s -e --opt -c %s" + \
                          " --ignore-table=mysql.event | " + \
                          "gzip -c > %s.gz") % (self.login_info["username"],
                                                self.login_info["password"],
                                                self.login_info["host"],
                                                database,
                                                filename))
