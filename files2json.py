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
    data = {name: (dir2dict if isdir(name) else file2list)(name)
            for name in listdir('.')}
    chdir('..')
    return data

  def file2list(filename):
    """
    filename: str -> contents: list
    """
    return patt.sub(repl, open(filename).read()).splitlines()

  data = {root_dir: dir2dict(root_dir)}
  return data



if __name__=='__main__':

  print(__doc__)

  root = 'test_files'
  print __import__('json').dumps(files2json(root), indent=2)

  '''
  {
    "test_files": {
      "labmate": {
        "graduated_phd.name": [
          "graduated_phd1@domain1", 
          "graduated_phd2@domain2", 
          "graduated_phd3@domain3"
        ], 
        "meeting.name": [
          "meeting1@domain1", 
          ":include:./labmate/phd.name", 
          "102g", 
          "103g", 
          "meeting1@domain2"
        ], 
        "test.name": [
          "test@test.domain"
        ], 
        "all_students.name": [
          "student1@domain1", 
          "alumni", 
          ":include:./labmate/phd.name", 
          "102g", 
          "103g"
        ], 
        "100g.name": [
          "100g1@domain1", 
          "100g2@domain2"
        ], 
        "phd.name": [
          "phd1@domain1", 
          "phd2@domain2", 
          "phd3@domain3"
        ], 
        "alumni.name": [
          "alumni1@domain1", 
          "100g", 
          "alumni2@domain2", 
          "101g", 
          "alumni3@domain3"
        ], 
        "102g.name": [
          "102g1@domain1", 
          "102g2@domain2"
        ], 
        "103g.name": [
          "103g1@domain1", 
          "103g2@domain2"
        ], 
        "101g.name": [
          "101g1@domain1", 
          "101g2@domain2"
        ]
      }, 
      "aliases": [
        "100g:   :include:./labmate/100g.name", 
        "101g:   :include:./labmate/101g.name", 
        "102g:   :include:./labmate/102g.name", 
        "103g:   :include:./labmate/103g.name", 
        "phd:    :include:./labmate/phd.name", 
        "meeting: :include:./labmate/meeting.name", 
        "graduated_phd:  :include:./labmate/graduated_phd.name", 
        "", 
        "MAILER-DAEMON: postmaster", 
        "Postmaster: root", 
        "all_students:   :include:./labmate/all_students.name", 
        "alumni: :include:./labmate/alumni.name     ", 
        "", 
        "root: admin@domain1, admin@domain2", 
        "test:  :include:./labmate/test.name", 
        "nobody: /dev/null", 
        ""
      ]
    }
  }
  '''
