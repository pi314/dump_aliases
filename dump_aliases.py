"""
usage:
  $cmd $aliases_file_path

issues:
  - assume that the aliases file has passed ``postalias``
  - use ``argparse`` to get arguments
  - store all error/warning(s) and output it.
  - use unittest but doctest to avoid charactor escaping problems.

doctest:
  >>> content = '''
  ... # user2 : something , name@domain, |cmd, " | cmd2 arg" , :include:   another_file
  ... user  : something , name@domain, |cmd, " | cmd2 arg" , :include:   another_file
  ... '''
"""


import re


def parse_aliases(aliases_content):
  '''
  aliases_content -> cleaned -> split to key-value parts -> completed value part

  str -> [(key, [v1, v2, v3, ...]), ...]
  '''
  result = sorted((key, parse_values(values)) for key, values in split(cleaned( aliases_content )))
  return result


def cleaned(content):
  '''
  - remove slash and concatenate with next line
  - remove all comments
  - remove blank lines
  - return a list containing meaningful records
  '''
  content = re.sub(r'\\[\n\r]', '', content)
  content = re.sub(r'#.*$', '', content, flags=re.M)
  content = re.sub(r'^\s*', '', content, flags=re.M)
  
  #print repr(content)
