"""
Warning:
  This program is designed for absolute path and local files but soft-link
  files. It will cause unexpected error if there are soft-link or related
  path.
"""


import argparse
import re
from os import getcwd, chdir, listdir
from os.path import isdir, abspath


def files2json(root_dir):
  """
  given root directory, collecting all files' contents to
  one python script with Python dict and string formatting
  """

  root_path = abspath(root_dir)

  patt = re.compile(r'([^"#]*)("(?:[^"#]*(?:#.*$)?)*")?(#.*$)?', flags=re.M|re.S)
  blank = lambda s: s.replace(root_path, "{root_path}")
  repl = lambda m: (m.group(1)) + (m.group(2) or '') + (m.group(3) or '')

  def dir2dict(dirname):
    """
    dirname: str -> data: dict
    """
    chdir(dirname)
    data = {name: (dir2dict if isdir(name) else file2str)(name)
            for name in listdir('.')}
    chdir('..')
    return data

  def file2list(filename):
    """
    filename: str -> contents: list
    """
    return open(filename).readlines()

  def file2str(filename):
    """
    filename: str -> modified contents: str
    """
    return patt.sub(repl, open(filename).read())

  data = {root_dir: dir2dict(root_dir)}
  return data



if __name__=='__main__':

  print(__doc__)

  root = 'test_files'
  print __import__('json').dumps(files2json(root), indent=2)
