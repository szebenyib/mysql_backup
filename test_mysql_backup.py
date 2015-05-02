import time
import os
import unittest
import mysql_backup

configpath = "/etc/mysql/debian.cnf"
backuppath = "/mnt/user_szebenyib/backups/mysql"

class TestBackupCreation(unittest.TestCase):

    def setUp(self):
        self.configpath = configpath
        self.backuppath = backuppath

    def tearDown(self):
        del self.configpath
        del self.backuppath

    def test_create_class(self):
        mb = mysql_backup.Backup()

class TestBackupMethods(unittest.TestCase):

    def setUp(self):
        self.configpath = configpath
        self.backuppath = backuppath
        self.mb = mysql_backup.Backup()

    def tearDown(self):
        del self.configpath
        del self.backuppath

    def test_set_filestamp(self):
        self.mb.set_filestamp()
        self.assertIsNotNone(self.mb.filestamp)
        self.assertEqual(self.mb.filestamp, time.strftime("%Y-%m-%d"))

    def test_read_config_permissions(self):
        with self.assertRaises(OSError):
            os.stat(self.configpath + "ASDASDASD.LLLL")
        try:
            os.stat(self.configpath)
        except:
            self.fail("Check the path variable in the test file," + \
                      "it should be readable: " + self.configpath)

    def test_read_config_creates_dictionary(self):
        self.mb.read_config(config_location=self.configpath)
        self.assertIsInstance(self.mb.login_info,
                              dict)

    def test_read_config_read_default_location(self):
        self.mb.read_config(config_location=self.configpath)
        login_info = self.mb.login_info
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_read_config_read_nondefault_location(self):
        self.mb.read_config(config_location=self.configpath)
        login_info = self.mb.login_info
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_get_list_of_databases_returns_a_list(self):
        self.mb.read_config(config_location=self.configpath)
        login_info = self.mb.login_info
        self.assertIsInstance(self.mb.get_list_of_databases(), list)

    def test_get_list_of_databases_not_empty(self):
        self.mb.read_config(config_location=self.configpath)
        login_info = self.mb.login_info
        list_of_databases = self.mb.get_list_of_databases()
        self.assertTrue(len(list_of_databases) > 0)

    def test_get_filename_of_backup_is_string(self):
        self.mb.read_config(config_location=self.configpath)
        login_info = self.mb.login_info
        list_of_databases = self.mb.get_list_of_databases()
        database = "a"
        filestamp = self.mb.filestamp
        self.assertIsInstance(self.mb.get_filename_of_backup(self.configpath,
                                                             database,
                                                             filestamp), str)

    def test_get_filename_trailing_slash(self):
        self.mb.read_config(config_location=self.configpath)
        login_info = self.mb.login_info
        list_of_databases = self.mb.get_list_of_databases()
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
        self.mb.read_config(config_location=self.configpath)
        login_info = self.mb.login_info
        list_of_databases = self.mb.get_list_of_databases()
        filestamp = self.mb.filestamp
        databases = self.mb.get_list_of_databases()
        self.mb.backup_databases(database_list=databases,
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
