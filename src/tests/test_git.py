import unittest
import sys
sys.path.insert(1, '..')
import git

GH_SSH_FINGERPRINTS = '''
github.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk=
github.com ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg=
github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
'''
GH_SSH_FINGERPRINTS = GH_SSH_FINGERPRINTS[1:]

class TestGitLeaks(unittest.TestCase):
    def test_get_ssh_fingerprint(self):
        self.assertEqual('',
            git.get_ssh_fingerprint(
                'git@nope.com:Techno-Hwizrdry/checkpwnedemails.git'
            )
        )
        self.assertEqual(GH_SSH_FINGERPRINTS,
            git.get_ssh_fingerprint(
                'git@github.com:Techno-Hwizrdry/checkpwnedemails.git'
            )
        )
        self.assertEqual('', git.get_ssh_fingerprint(''))
        self.assertEqual('', git.get_ssh_fingerprint(None))
        self.assertEqual('', git.get_ssh_fingerprint('checkpwnedemails.git'))
        self.assertEqual('',
            git.get_ssh_fingerprint(
                'https://github.com/Techno-Hwizrdry/checkpwnedemails.git'
            )
        )

    def test_read_known_hosts(self):
        self.assertEqual(
            tuple(GH_SSH_FINGERPRINTS.strip().split('\n')),
            git.read_known_hosts('github.com.txt')
        )
        
    def test_is_valid_git_link(self):
        self.assertFalse(git.is_valid_git_link('.'))
        self.assertTrue(git.is_valid_git_link(
                'git@github.com:Techno-Hwizrdry/checkpwnedemails.git'
            )
        )
        self.assertTrue(git.is_valid_git_link(
                'https://github.com/Techno-Hwizrdry/checkpwnedemails.git'
            )
        )
        self.assertTrue(git.is_valid_git_link(
                'git@gitlab.com:inkscape/inkscape.git'
            )
        )
        self.assertTrue(git.is_valid_git_link(
                'https://gitlab.com/inkscape/inkscape.git'
            )
        )
        self.assertFalse(git.is_valid_git_link(
                'invalid_repo_link.git'
            )
        )
        self.assertFalse(git.is_valid_git_link(
                'https://gitlab.com/inkscape/'
            )
        )
        self.assertFalse(git.is_valid_git_link(
                'gitlab.com/inkscape/inkscape.git'
            )
        )
        self.assertFalse(git.is_valid_git_link(
                'inkscape/inkscape.git'
            )
        )
        self.assertFalse(git.is_valid_git_link(''))
        self.assertFalse(git.is_valid_git_link(None))
        self.assertFalse(git.is_valid_git_link('/dir/does/not/exist'))
        self.assertFalse(git.is_valid_git_link('#!\'"'))

    def test__all_in_b(self):
        a = [1, 12, 23]
        b = [9, 1, 77, 23, 12]
        self.assertTrue(git._all_in_b(a, b))
        self.assertTrue(git._all_in_b(b, a))
        self.assertFalse(git._all_in_b((55, 100, 2000), b))

if __name__ == "__main__":
    unittest.main()
