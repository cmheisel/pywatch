import os
import time
import unittest

from watcher import Watcher

class WatcherTest(unittest.TestCase):
    def touch(self, filename):
        os.utime(filename, None)

    def setUp(self):
        self.watcher = Watcher(cmds = ["python fixtures/sample.py", ])

    def tearDown(self):
        del(self.watcher)

    def test_add_files(self):
        """When files are added, either at init or via add_files
        watcher.files length should reflect that. Non-files or duplicates
        shouldn't be reflected."""
        
        self.assertEqual(0, len(self.watcher.files))
        self.watcher.add_files("fixtures/a.txt", "fixtures/b.txt")
        self.assertEqual(2, len(self.watcher.files))
       
        self.watcher.add_files("fixtures/c.txt")
        self.assertEqual(3, len(self.watcher.files))

        w = Watcher(files=["fixtures/a.txt", "fixtures/b.txt", "fixtures/c.txt"])
        self.assertEqual(3, len(w.files))
   
    def test_add_cmds(self):
        """When files are added, either at init or via add_cmds
        watcher.cmds length should reflect that. Non-files or duplicates
        shouldn't be reflected."""
       
        w = Watcher()
        self.assertEqual(0, len(w.cmds))
        w.add_cmds("python fixtures/sample.py", "./fixtures/sample.py")
        self.assertEqual(2, len(w.cmds))
       

        w = Watcher(cmds=["python fixtures/sample.py"])
        self.assertEqual(1, len(w.cmds))


    def test_file_monitoring(self):
        """Files that are touched should trigger an execution. watcher.num_runs
        should reflect the number of times this Watcher instance has executed
        its command list."""

        self.assertEqual(0, self.watcher.num_runs)

        self.watcher.add_files("fixtures/a.txt", "fixtures/b.txt")
        self.assertEqual(0, self.watcher.num_runs)

        self.touch("fixtures/a.txt") 
        self.watcher.monitor_once()
        self.assertEqual(1, self.watcher.num_runs)

        self.touch("fixtures/b.txt")
        self.watcher.monitor_once()
        self.assertEqual(2, self.watcher.num_runs)

        self.watcher.monitor_once()
        self.assertEqual(2, self.watcher.num_runs)

    def test_continous_file_monitoring(self):
        """Watcher.monitor() should run continously executing the command
        list whenever files change."""

        self.watcher.add_files("fixtures/a.txt", "fixtures/b.txt", "fixtures/c.txt")
        self.watcher.monitor()

        self.touch("fixtures/a.txt")
        time.sleep(1)
        self.assertEqual(1, self.watcher.num_runs)
        
        self.watcher.stop_monitor()

if __name__ == "__main__":
    unittest.main()
