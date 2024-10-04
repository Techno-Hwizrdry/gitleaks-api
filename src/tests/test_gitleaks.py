import unittest
import sys
sys.path.insert(1, '..')
from gitleaks import GitLeaks
from config import Settings

class TestGitLeaks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = Settings()
        cls.gitleaks = GitLeaks(config.gitleaks_path)

    def test_detect(self):
        SUCCESS = 200
        ssh = 'git@github.com:Techno-Hwizrdry/netscan.git'
        https = 'https://github.com/Techno-Hwizrdry/netscan.git'
        ssh_results = self.gitleaks.detect(ssh)
        https_results = self.gitleaks.detect(https)
        self.assertEqual(SUCCESS, ssh_results['status_code'])
        self.assertEqual('Success', ssh_results['message'])
        self.assertNotEqual(None, ssh_results['output'])

        self.assertEqual(SUCCESS, https_results['status_code'])
        self.assertEqual('Success', https_results['message'])
        self.assertNotEqual(None, https_results['output'])

        invalid = {
            'status_code': 400,
            'message': 'Invalid git link',
            'output': None
        }
        self.assertEqual(invalid, self.gitleaks.detect('invalidlink.com'))

    def test__parse_output_no_leaks(self):
        test_output = '\x1b[90m7:22PM\x1b[0m \x1b[32mINF\x1b[0m 20 commits scanned.\n\x1b[90m7:22PM\x1b[0m \x1b[32mINF\x1b[0m scan completed in 30.9ms\n\x1b[90m7:22PM\x1b[0m \x1b[32mINF\x1b[0m no leaks found\n'
        expected = '7:22PM INF 20 commits scanned.\n7:22PM INF scan completed in 30.9ms\n7:22PM INF no leaks found\n'
        self.assertEqual(expected, self.gitleaks._parse_output(test_output))

if __name__ == "__main__":
    unittest.main()