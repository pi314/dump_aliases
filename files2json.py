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

  def dir2dict(dirname):
    """
    dirname: str -> data: dict
    """
    chdir(dirname)
    data = {name: (dir2dict if isdir(name) else file2list)(name) for name in listdir('.')}
    chdir('..')
    return data

  def file2list(filename):
    """
    filename: str -> contents: list
    """
    return patt.sub(repl, open(filename).read()).splitlines()

  root_path = abspath(root_dir)
  patt = re.compile(r'([^"#]*)("(?:[^"#]*(?:#.*$)?)*")?(#.*$)?', flags=re.M|re.S)
  blank = lambda s: s.replace('{','{{').replace('}','}}').replace(root_path, "{root_path}")
  repl = lambda m: blank(m.group(1)) + (m.group(2) or '') + (m.group(3) or '')
  return dir2dict(root_dir)


if __name__=='__main__':

  from argparse import ArgumentParser
  from json import dumps
  from sys import stderr
  parser = ArgumentParser()
  parser.add_argument('root_dir')
  root_dir = parser.parse_args().root_dir
  stderr.write(__doc__)
  stderr.write('\n')
  print(dumps(files2json(root_dir),indent=2))
