"""
This program will collect all files to one JSON file,
and transform the path of ``:include:`` as Python string
format parameters.
If there are some files nothing to do, they will be
collected, too. Run this program carefully!!
"""


import os
import argparse
from os.path import isdir


def files2json(root_dir):
  """
  given root directory, collecting all files' contents to
  one python script with Python dict and string formatting
  """

  def dir2dict(dirname):
    """
    dirname: str -> data: dict
    """
    os.chdir(dirname)
    data = {name: (dir2dict if isdir(name) else file2list)(name)
            for name in os.listdir('.')}
    os.chdir('..')
    return data

  def file2list(filename):
    """
    filename: str -> contents: list
    """
    return open(filename).readlines()

  data = {root_dir: dir2dict(root_dir)}
  return data


from pprint import pprint as p

root = '.'
root = 'test_files'
p(files2json(root))
