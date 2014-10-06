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



if __name__=='__main__':
	root = 'test_files'
	print __import__('json').dumps(files2json(root), indent=2)

	"""
	{
		"test_files": {
			"labmate": {
				"graduated_phd.name": [
					"graduated_phd1@domain1\n",
					"graduated_phd2@domain2\n",
					"graduated_phd3@domain3\n"
				],
				"meeting.name": [
					"meeting1@domain1\n",
					":include:./labmate/phd.name\n",
					"102g\n",
					"103g\n",
					"meeting1@domain2\n"
				],
				"test.name": [
					"test@test.domain\n"
				],
				"all_students.name": [
					"student1@domain1\n",
					"alumni\n",
					":include:./labmate/phd.name\n",
					"102g\n",
					"103g\n"
				],
				"100g.name": [
					"100g1@domain1\n",
					"100g2@domain2\n"
				],
				"phd.name": [
					"phd1@domain1\n",
					"phd2@domain2\n",
					"phd3@domain3\n"
				],
				"alumni.name": [
					"alumni1@domain1\r\n",
					"100g\r\n",
					"alumni2@domain2\r\n",
					"101g\r\n",
					"alumni3@domain3\r\n"
				],
				"102g.name": [
					"102g1@domain1\n",
					"102g2@domain2\n"
				],
				"103g.name": [
					"103g1@domain1\n",
					"103g2@domain2\n"
				],
				"101g.name": [
					"101g1@domain1\n",
					"101g2@domain2\n"
				]
			},
			"aliases": [
				"100g:   :include:./labmate/100g.name\n",
				"101g:   :include:./labmate/101g.name\n",
				"102g:   :include:./labmate/102g.name\n",
				"103g:   :include:./labmate/103g.name\n",
				"phd:    :include:./labmate/phd.name\n",
				"meeting: :include:./labmate/meeting.name\n",
				"graduated_phd:  :include:./labmate/graduated_phd.name\n",
				"\n",
				"MAILER-DAEMON: postmaster\n",
				"Postmaster: root\n",
				"all_students:   :include:./labmate/all_students.name\n",
				"alumni: :include:./labmate/alumni.name     \n",
				"\n",
				"root: admin@domain1, admin@domain2\n",
				"test:  :include:./labmate/test.name\n",
				"nobody: /dev/null\n",
				"\n"
			]
		}
	}
	"""
