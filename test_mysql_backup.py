import time
import os
import ConfigParser
import imp
import unittest
import mysql_backup

config = ConfigParser.ConfigParser()
config.read("config.txt")
configpath = config.get("backup", "configpath")
backuppath = config.get("backup", "backuppath")

class TestBackupCreation(unittest.TestCase):

    def setUp(self):
        self.configpath = configpath
        self.backuppath = backuppath

    def tearDown(self):
        del self.configpath
        del self.backuppath

    def test_create_class(self):
        mb = mysql_backup.Backup(self.configpath,
                                 self.backuppath)
        self.assertIsInstance(mb, mysql_backup.Backup)

    def test_correct_path(self):
        with self.assertRaises(OSError):
                mb = mysql_backup.Backup(self.configpath + "ASDASD.LLLL",
                                         self.backuppath)

    def test_check_path(self):
        with self.assertRaises(OSError):
                mb = mysql_backup.Backup(self.configpath,
                                         self.backuppath + "ASDASD.LLLL")
    def test_set_filestamp(self):
        mb = mysql_backup.Backup(self.configpath,
                                 self.backuppath)
        self.assertIsNotNone(mb.filestamp)
        self.assertEqual(mb.filestamp, time.strftime("%Y-%m-%d"))

class TestBackupMethods(unittest.TestCase):

    def setUp(self):
        self.configpath = configpath
        self.backuppath = backuppath
        self.mb = mysql_backup.Backup(self.configpath,
                                      self.backuppath)

    def tearDown(self):
        del self.configpath
        del self.backuppath

    def test_read_config_permissions(self):
        with self.assertRaises(OSError):
            os.stat(self.configpath + "ASDASDASD.LLLL")
        try:
            os.stat(self.configpath)
        except:
            self.fail("Check the path variable in the test file," + \
                      "it should be readable: " + self.configpath)

    def test_read_config_creates_dictionary(self):
        self.mb.read_config()
        self.assertIsInstance(self.mb.login_info,
                              dict)

    def test_read_config_read_default_location(self):
        self.mb.read_config()
        login_info = self.mb.login_info
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_read_config_read_nondefault_location(self):
        self.mb.read_config()
        login_info = self.mb.login_info
        keys = login_info.keys()
        self.assertTrue("username" in keys)
        self.assertTrue("password" in keys)
        self.assertTrue("host" in keys)

    def test_read_list_of_databases_returns_a_list(self):
        self.mb.read_config()
        login_info = self.mb.login_info
        self.mb.read_list_of_databases()
        self.assertIsInstance(self.mb.database_list, list)

    def test_read_list_of_databases_not_empty(self):
        self.mb.read_config()
        login_info = self.mb.login_info
        self.mb.read_list_of_databases()
        self.assertTrue(len(self.mb.database_list) > 0)

    def test_get_filename_of_backup_is_string(self):
        self.mb.read_config()
        login_info = self.mb.login_info
        database = "a"
        filestamp = self.mb.filestamp
        self.assertIsInstance(self.mb.get_filename_of_backup(database), str)

    def test_backup_databases_creates_file(self):
        self.mb.read_config()
        login_info = self.mb.login_info
        self.mb.read_list_of_databases()
        filestamp = self.mb.filestamp
        self.mb.backup_databases()
        try:
            filename = self.mb.get_filename_of_backup(database="mysql")
            filename = filename + ".gz"
            os.stat(filename)
        except:
            self.fail("No mysql backup created as of today: " + \
                      filename + " does not exist at: " + \
                      self.backuppath)

    def test_running_backup(self):
        mysql_backup.backup()

if __name__ == "main":
    unittest.main()
