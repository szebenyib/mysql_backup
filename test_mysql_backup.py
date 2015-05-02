import time
import os
import unittest
import mysql_backup

path = "/etc/mysql/debian.cnf"

class MyTest(unittest.TestCase):

    def test_create_class(self):
        mb = mysql_backup.Backup()

    def test_get_filestamp(self):
        mb = mysql_backup.Backup()
        self.assertIsNotNone(mb.get_filestamp())
        self.assertEqual(mb.get_filestamp(), time.strftime("%Y-%m-%d"))

    def test_read_config_permissions(self):
        with self.assertRaises(OSError):
            os.stat(path + "ASDASDASD.LLLL")
        try:
            os.stat(path)
        except:
            self.fail("Check the path variable in the test file," + \
                      "it should be readable: " + path)

    def test_read_config_returns_a_dictionary(self):
        mb = mysql_backup.Backup()
        self.assertIsInstance(mb.read_config(config_location=path), dict)

    def test_read_config_read_default_location(self):
        mb = mysql_backup.Backup()
        login_info = mb.read_config(config_location=path)
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_read_config_read_nondefault_location(self):
        mb = mysql_backup.Backup()
        login_info = mb.read_config(config_location=path)
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_get_list_of_databases_returns_a_list(self):
        mb = mysql_backup.Backup()
        login_info = mb.read_config(config_location=path)
        self.assertIsInstance(mb.get_list_of_databases(login_info), list)

    def test_get_list_of_databases_not_empty(self):
        mb = mysql_backup.Backup()
        login_info = mb.read_config(config_location=path)
        list_of_databases = mb.get_list_of_databases(login_info)
        self.assertTrue(len(list_of_databases) > 0)

    def test_get_filename_of_backup_is_string(self):
        mb = mysql_backup.Backup()
        login_info = mb.read_config(config_location=path)
        list_of_databases = mb.get_list_of_databases(login_info)
        backuppath = "/mnt/user_szebenyib/backups/mysql/"
        database = "a"
        filestamp = mb.get_filestamp()
        self.assertIsInstance(mb.get_filename_of_backup(backuppath,
                                                        database,
                                                        filestamp), str)

    def test_get_filename_trailing_slash(self):
        mb = mysql_backup.Backup()
        login_info = mb.read_config(config_location=path)
        list_of_databases = mb.get_list_of_databases(login_info)
        filestamp = mb.get_filestamp()
        database = "a"
        backuppath = "/mnt/user_szebenyib/backups/mysql"
        filename_w_trailing_slash = mb.get_filename_of_backup(backuppath,
                                                              database,
                                                              filestamp)
        backuppath = "/mnt/user_szebenyib/backups/mysql/"
        filename_wo_trailing_slash = mb.get_filename_of_backup(backuppath,
                                                               database,
                                                               filestamp)
        self.assertEquals(filename_w_trailing_slash,
                          filename_wo_trailing_slash)

    def test_backup_databases_creates_file(self):
        mb = mysql_backup.Backup()
        login_info = mb.read_config(config_location=path)
        list_of_databases = mb.get_list_of_databases(login_info)
        filestamp = mb.get_filestamp()
        databases = mb.get_list_of_databases(login_info=login_info)
        backuppath = "/mnt/user_szebenyib/backups/mysql/"
        mb.backup_databases(login_info=login_info,
                            database_list=databases,
                            backuppath=backuppath)
        try:
            filename = mb.get_filename_of_backup(path=backuppath,
                                                 database="mysql",
                                                 filestamp = filestamp)
            filename = filename + ".gz"
            os.stat(filename)
        except:
            self.fail("No mysql backup created as of today: " + \
                      filename + " does not exist at: " + \
                      backuppath)

if __name__ == "main":
    unittest.main()
