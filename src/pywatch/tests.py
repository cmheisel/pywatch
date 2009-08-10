import os
import time
import unittest

from pywatch.watcher import Watcher

class WatcherTest(unittest.TestCase):
    def touch(self, filename):
        os.utime(filename, None)

    def setUp(self):
        base_path = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
        self.fixtures_path = os.path.join(base_path, 'fixtures')
        self.watcher = Watcher()

    def tearDown(self):
        self.watcher.stop_monitor()
        del self.watcher

    def fixture(self, *filenames):
        return os.path.join(self.fixtures_path, *filenames)

    def test_directories(self):
        self.watcher.add_files(self.fixture("subdir"))
        self.assert_(len(self.watcher.files) > 1, "Expected more than 1 file, %s watched" % len(self.watcher.files))

        self.touch(self.fixture("subdir", "bar.txt")) 
        self.watcher.monitor_once()
        self.assertEqual(1, self.watcher.num_runs)

        self.touch(self.fixture("subdir", "subsubdir", "baz.txt"))
        self.watcher.monitor_once()
        self.assertEqual(2, self.watcher.num_runs)

    def test_add_files(self):
        """When files are added, either at init or via add_files
        watcher.files length should reflect that. Non-files or duplicates
        shouldn't be reflected."""
        
        self.assertEqual(0, len(self.watcher.files))
        self.watcher.add_files(self.fixture("a.txt"), self.fixture("b.txt"))
        self.assertEqual(2, len(self.watcher.files))
       
        self.watcher.add_files(self.fixture("c.txt"))
        self.assertEqual(3, len(self.watcher.files))

        w = Watcher(files=[self.fixture("a.txt"), self.fixture("b.txt"), self.fixture("c.txt")])
        self.assertEqual(3, len(w.files))
   
    def test_add_cmds(self):
        """When files are added, either at init or via add_cmds
        watcher.cmds length should reflect that. Non-files or duplicates
        shouldn't be reflected."""
       
        w = Watcher()
        self.assertEqual(0, len(w.cmds))
        w.add_cmds("python %s" % self.fixture('sample.py'), self.fixture('sample.py'))
        self.assertEqual(2, len(w.cmds))
       

        w = Watcher(cmds=["python %s" % self.fixture('sample.py')])
        self.assertEqual(1, len(w.cmds))


    def test_file_monitoring(self):
        """Files that are touched should trigger an execution. watcher.num_runs
        should reflect the number of times this Watcher instance has executed
        its command list."""

        self.assertEqual(0, self.watcher.num_runs)

        self.watcher.add_files(self.fixture("a.txt"), self.fixture("b.txt"))
        self.assertEqual(0, self.watcher.num_runs)

        self.touch(self.fixture("a.txt")) 
        self.watcher.monitor_once()
        self.assertEqual(1, self.watcher.num_runs)

        self.touch(self.fixture("b.txt"))
        self.watcher.monitor_once()
        self.assertEqual(2, self.watcher.num_runs)

        self.watcher.monitor_once()
        self.assertEqual(2, self.watcher.num_runs)

    def test_continous_file_monitoring(self):
        """Watcher.monitor() should run continously executing the command
        list whenever files change."""

        self.watcher.add_files(self.fixture("a.txt"), self.fixture("b.txt"), self.fixture("c.txt"))
        self.watcher.monitor()

        self.touch(self.fixture("a.txt"))
        time.sleep(2)
        self.assertEqual(1, self.watcher.num_runs)
        
        self.watcher.stop_monitor()

def test_suite():
    return unittest.makeSuite(WatcherTest)

if __name__ == "__main__":
    unittest.main()
