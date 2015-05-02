#!/usr/bin/env python
# Source: http://codepoets.co.uk/2010/python-script-to-backup-mysql-databases-on-debian/
import os
import time
import ConfigParser
import unittest

class Backup():
    def get_filestamp(self):
        """Obtains a date stamp for the files from the date.
        @return: a string YYYY-MM-DD
        """
        return time.strftime("%Y-%m-%d")

    def read_config(self, config_location="/etc/mysql/debian.cnf"):
        """Reads the databse config from its location. The default
        is the place where the config file is found on debian based systems
        including Ubuntu.
        @param: config_location is by default "/etc/mysql/debian.cnf"
        @return a dictionary with "user", "password", "host"
        """
        config = ConfigParser.ConfigParser()
        try:
            os.stat(config_location)
        except OSError:
            raise OSError
        config.read(config_location)
        login_info = dict()
        login_info["username"] = config.get("client", "user")
        login_info["password"] = config.get("client", "password")
        login_info["host"] = config.get("client", "host")
        return login_info

    def get_list_of_databases(self, login_info):
        database_list_command = ("mysql -u %s -p%s -h %s --silent -N" + \
                                 " -e 'show databases'") % (
                                 login_info["username"],
                                 login_info["password"],
                                 login_info["host"])
        f = os.popen(database_list_command, 'r')
        database_list = f.readlines()
        return database_list

    def get_filename_of_backup(self, path, database, filestamp):
        last_char_of_path = path[len(path) - 1]
        if last_char_of_path != "/":
            path = path + "/"
        filename = (path + "%s-%s.sql") % (database, filestamp)
        return filename

    def backup_databases(self, login_info, database_list, backuppath):
            for database in database_list:
                database = database.strip()
                filestamp = self.get_filestamp()
                if database not in ["information_schema",
                                    "performance_schema"]:
                    filename = self.get_filename_of_backup(path=backuppath,
                                                           database=database,
                                                           filestamp=filestamp)
                    try:
                        os.stat(backuppath)
                    except OSError:
                        print "Not writable: " + filename
                        raise OSError
                    os.popen(("mysqldump -u %s -p%s -h %s -e --opt -c %s" + \
                              " --ignore-table=mysql.event | " + \
                              "gzip -c > %s.gz") % (login_info["username"],
                                                    login_info["password"],
                                                    login_info["host"],
                                                    database,
                                                    filename))
