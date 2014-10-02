from dump_aliases import *

from pprint import pformat
import os
import unittest


class TestDumpAliases(unittest.TestCase):

  def setUp(self):
    os.chdir('test_files')
    self.aliases_file = 'aliases'

  def test_given_files(self):
    from textwrap import dedent
    expected_output = '''
      100g:100g1@domain1
      100g:100g2@domain2
      101g:101g1@domain1
      101g:101g2@domain2
      102g:102g1@domain1
      102g:102g2@domain2
      103g:103g1@domain1
      103g:103g2@domain2
      MAILER-DAEMON:postmaster
      Postmaster:root
      all_students:102g
      all_students:103g
      all_students:alumni
      all_students:phd1@domain1
      all_students:phd2@domain2
      all_students:phd3@domain3
      all_students:student1@domain1
      alumni:100g
      alumni:101g
      alumni:alumni1@domain1
      alumni:alumni2@domain2
      alumni:alumni3@domain3
      graduated_phd:graduated_phd1@domain1
      graduated_phd:graduated_phd2@domain2
      graduated_phd:graduated_phd3@domain3
      meeting:102g
      meeting:103g
      meeting:meeting1@domain1
      meeting:meeting1@domain2
      meeting:phd1@domain1
      meeting:phd2@domain2
      meeting:phd3@domain3
      nobody:/dev/null
      phd:phd1@domain1
      phd:phd2@domain2
      phd:phd3@domain3
      root:admin@domain1
      root:admin@domain2
      test:test@test.domain
    '''
    expected_data = dedent(expected_output).split()
    dumped_data = main(self.aliases_file)
    self.assertEqual(len(expected_data), len(dumped_data),
                     msg="dumped_data =\n"+pformat(dumped_data))
    for a, b in zip(expected_data, dumped_data):
      self.assertEqual(a, ':'.join(b))


if __name__=='__main__':
  unittest.main()
