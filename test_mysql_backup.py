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
numbertokeep = config.get("delete", "numbertokeep")

class TestBackupCreation(unittest.TestCase):

    def setUp(self):
        self.configpath = configpath
        self.backuppath = backuppath
        self.numbertokeep = numbertokeep

    def tearDown(self):
        del self.configpath
        del self.backuppath
        del self.numbertokeep

    def test_create_class(self):
        mb = mysql_backup.Backup(self.configpath,
                                 self.backuppath,
                                 self.numbertokeep)
        self.assertIsInstance(mb, mysql_backup.Backup)

    def test_correct_path(self):
        with self.assertRaises(OSError):
                mb = mysql_backup.Backup(self.configpath + "ASDASD.LLLL",
                                         self.backuppath,
                                         self.numbertokeep)

    def test_check_path(self):
        with self.assertRaises(OSError):
                mb = mysql_backup.Backup(self.configpath,
                                         self.backuppath + "ASDASD.LLLL",
                                         self.numbertokeep)
    def test_set_filestamp(self):
        mb = mysql_backup.Backup(self.configpath,
                                 self.backuppath,
                                 self.numbertokeep)
        self.assertIsNotNone(mb.filestamp)
        self.assertEqual(mb.filestamp, time.strftime("%Y-%m-%d"))

class TestBackupMethods(unittest.TestCase):

    def setUp(self):
        self.configpath = configpath
        self.backuppath = backuppath
        self.numbertokeep = numbertokeep
        self.mb = mysql_backup.Backup(self.configpath,
                                      self.backuppath,
                                      self.numbertokeep)

    def tearDown(self):
        del self.configpath
        del self.backuppath
        del self.numbertokeep
        del self.mb

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

#class TestBackupDeletion(unittest.TestCase):
#
#    def setUp(self):
#        self.configpath = configpath
#        self.backuppath = backuppath
#        self.numbertokeep = numbertokeep
#        self.mb = mysql_backup.Backup(self.configpath,
#                                      self.backuppath,
#                                      self.numbertokeep)
#        self.mb.read_config()
#        self.mb.read_list_of_databases()
#        self.mb.backup_databases()
#
#    def tearDown(self):
#        del self.configpath
#        del self.backuppath
#        del self.numbertokeep
#        del self.mb
#
#    def test_delete_old_backups(self):
#        files_list = []
#        for f in os.listdir(self.backuppath):
#            full_path = os.path.join(self.backuppath, f)
#            if os.path.isfile(full_path):
#                files_list.append((full_path,
#                                   os.path.getmtime(full_path)))
#        print files_list

if __name__ == "main":
    unittest.main()
