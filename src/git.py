import os
import re
import pathlib
import subprocess
from typing import Union

def add_ssh_fingerprint(git_link: str) -> None:
    '''
    Adds the SSH fingerprints of git_link to ~/.ssh/known_hosts.
    If it already exists, then do nothing and return.
    '''
    ssh_fp = get_ssh_fingerprint(git_link)
    if not ssh_fp: return

    home_dir = str(pathlib.Path.home())
    known_hosts_path = os.path.join(home_dir, ".ssh", "known_hosts")
    if not os.path.isfile(known_hosts_path): return

    finger_prints = tuple(ssh_fp.split('\n'))
    know_hosts_fp = read_known_hosts(known_hosts_path)

    if not _all_in_b(finger_prints, know_hosts_fp):
        with open(known_hosts_path, 'a') as outfile:
            outfile.write(f'\n{ssh_fp}')

def clone(git_link: str) -> str:
    '''
    Clones the repo, if it doesn't exist locally.
    Returns name of the repo's directory.
    '''
    repo_name = git_link[git_link.rfind('/') + 1 : git_link.rfind('.')]
    if os.path.isdir(repo_name): return repo_name

    add_ssh_fingerprint(git_link)
    cmd = ('git', 'clone', git_link)
    subprocess.run(cmd)
    return repo_name

def get_ssh_fingerprint(git_link: str) -> str:
    '''
    Return SSH fringerprint of git_link, if it's a valid SSH.
    Otherwise return a blank string.  If no SSH fingerprint
    is found, then return a blank string.
    '''
    if not git_link or not _is_valid_ssh_git_link(git_link): return ''

    url = git_link[git_link.find('@') + 1 : git_link.find(':')]
    cmd = ('ssh-keyscan', url)
    result = subprocess.run(cmd, capture_output = True, text = True)
    return result.stdout

def is_valid_git_link(git_link: str) -> bool:
    '''
    Returns True if git_link is a valid HTTPS or SSH link.
    '''
    if not git_link: return False
    if _is_valid_ssh_git_link(git_link): return True

    return _is_valid_https_git_link(git_link)

def read_known_hosts(known_hosts_path: str) -> tuple[str]:
    '''
    Reads the .ssh/known_hosts file from know_hosts_path.
    If unsuccessful, return a blank string.
    '''
    if os.path.isfile(known_hosts_path):
        with open(known_hosts_path, 'r') as infile:
            raw_lines = infile.readlines()
            lines = [line.strip() for line in raw_lines if line.strip()]
            return tuple(lines)

    return ''

def _all_in_b(a: Union[list, tuple], b: Union[list, tuple]) -> bool:
    '''
    Returns True if all elements in list a are present in list b.
    '''
    set_a = set(a)
    set_b = set(b)
    if len(set_a) < len(set_b): return set_a.issubset(set_b)

    return set_b.issubset(set_a)

def _is_valid_ssh_git_link(git_link: str) -> bool:
    pattern = r"git@[a-zA-Z0-9\-]+\.[a-zA-Z0-9]+\:[a-zA-Z0-9\-]+\/[a-zA-Z0-9\-]+\.git"
    return re.match(pattern, git_link) is not None

def _is_valid_https_git_link(git_link: str) -> bool:
    pattern = r"https://[a-zA-Z0-9\-]+\.[a-zA-Z0-9]+\/[a-zA-Z0-9\-]+\/[a-zA-Z0-9\-]+\.git"
    return re.match(pattern, git_link) is not None