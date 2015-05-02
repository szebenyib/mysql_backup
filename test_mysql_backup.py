import time
import os
import unittest
import mysql_backup


class TestBackupCreation(unittest.TestCase):

    def setUp(self):
        self.path = "/etc/mysql/debian.cnf"
        self.backuppath = "/mnt/user_szebenyib/backups/mysql"

    def tearDown(self):
        del self.path
        del self.backuppath

    def test_create_class(self):
        mb = mysql_backup.Backup()

class TestBackupMethods(unittest.TestCase):

    def setUp(self):
        self.path = "/etc/mysql/debian.cnf"
        self.backuppath = "/mnt/user_szebenyib/backups/mysql"
        self.mb = mysql_backup.Backup()

    def tearDown(self):
        del self.path
        del self.backuppath

    def test_set_filestamp(self):
        self.mb.set_filestamp()
        self.assertIsNotNone(self.mb.filestamp)
        self.assertEqual(self.mb.filestamp, time.strftime("%Y-%m-%d"))

    def test_read_config_permissions(self):
        with self.assertRaises(OSError):
            os.stat(self.path + "ASDASDASD.LLLL")
        try:
            os.stat(self.path)
        except:
            self.fail("Check the path variable in the test file," + \
                      "it should be readable: " + self.path)

    def test_read_config_returns_a_dictionary(self):
        self.assertIsInstance(self.mb.read_config(config_location=self.path),
                              dict)

    def test_read_config_read_default_location(self):
        login_info = self.mb.read_config(config_location=self.path)
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_read_config_read_nondefault_location(self):
        login_info = self.mb.read_config(config_location=self.path)
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_get_list_of_databases_returns_a_list(self):
        login_info = self.mb.read_config(config_location=self.path)
        self.assertIsInstance(self.mb.get_list_of_databases(login_info), list)

    def test_get_list_of_databases_not_empty(self):
        login_info = self.mb.read_config(config_location=self.path)
        list_of_databases = self.mb.get_list_of_databases(login_info)
        self.assertTrue(len(list_of_databases) > 0)

    def test_get_filename_of_backup_is_string(self):
        login_info = self.mb.read_config(config_location=self.path)
        list_of_databases = self.mb.get_list_of_databases(login_info)
        database = "a"
        filestamp = self.mb.filestamp
        self.assertIsInstance(self.mb.get_filename_of_backup(self.path,
                                                             database,
                                                             filestamp), str)

    def test_get_filename_trailing_slash(self):
        login_info = self.mb.read_config(config_location=self.path)
        list_of_databases = self.mb.get_list_of_databases(login_info)
        filestamp = self.mb.filestamp
        database = "a"
        bad_backuppath = "/mnt/user_szebenyib/backups/mysql"
        fname_w_trailing_slash = self.mb.get_filename_of_backup(bad_backuppath,
                                                              database,
                                                              filestamp)
        good_backuppath = self.backuppath
        fname_wo_trailing_slash = self.mb.get_filename_of_backup(good_backuppath,
                                                               database,
                                                               filestamp)
        self.assertEquals(fname_w_trailing_slash,
                          fname_wo_trailing_slash)

    def test_backup_databases_creates_file(self):
        login_info = self.mb.read_config(config_location=self.path)
        list_of_databases = self.mb.get_list_of_databases(login_info)
        filestamp = self.mb.filestamp
        databases = self.mb.get_list_of_databases(login_info=login_info)
        self.mb.backup_databases(login_info=login_info,
                            database_list=databases,
                            backuppath=self.backuppath)
        try:
            filename = self.mb.get_filename_of_backup(path=self.backuppath,
                                                 database="mysql",
                                                 filestamp = filestamp)
            filename = filename + ".gz"
            os.stat(filename)
        except:
            self.fail("No mysql backup created as of today: " + \
                      filename + " does not exist at: " + \
                      self.backuppath)

if __name__ == "main":
    unittest.main()
