import re
import subprocess
from git import clone, is_valid_git_link
from typing import Dict

class GitLeaks:
    def __init__(self, exe_path: str) -> None:
        self.exe_path = exe_path

    def detect(self, git_link: str) -> Dict:
        if not is_valid_git_link(git_link):
            return self._json(400, 'Invalid git link')
        
        repo_name = clone(git_link)
        cmd = (self.exe_path, 'detect', '--no-banner', '.')
        result = subprocess.run(
            cmd,
            cwd=f'./{repo_name}',
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines = True
        )
        output = self._parse_output(result.stdout or result.stderr)
        return self._json(200, 'Success', output)
    
    def _json(self, status_code: int, msg: str, output: object=None) -> Dict:
        return {
            'status_code': status_code,
            'message': msg,
            'output': output
        }
    
    def _parse_output(self, gl_output: str) -> str:
        '''
        Parse gl_output for information regarding found secrets.
        If no leaks were found, then return an empty tuple.
        '''
        return self._remove_ANSI_escape_sequences(gl_output)

    def _remove_ANSI_escape_sequences(self, s: str) -> str:
        '''
        Returns s without any ANSI escape sequences.
        '''
        without_ansi = re.compile(r'\x1b[^m]*m')
        return without_ansi.sub('', s)