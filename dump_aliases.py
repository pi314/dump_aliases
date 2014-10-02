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


def cleaned(content):
  '''
  - remove slash and concatenate with next line
  - remove all comments
  - remove blank lines
  '''
  content = re.sub(r'#.*$', '', content, flags=re.M)
  content = re.sub(r'\\[\n\r]', '', content)
  content = re.sub(r'^\s*', '', content, flags=re.M)
  return content


def split2kv(line):
  '''
  only use for aliases file but other included files
  str -> [ {"key": str, "values": str} ]
  '''
  kv_patt = r"^\s*(?P<key>\S+?)\s*:\s*(?P<values>.+?)\s*$"
  #print(repr(line))
  result = re.findall(kv_patt, line, flags=re.M)
  #print(result)
  return result


def split_values(values):
  '''
  only use for included files
  str -> [ value ]
  '''
  #print('--->', values)
  result = []
  for value in re.split(r"\s*,\s*", values):
    m = re.match(r":include:\s*(?P<path>.*)", value)
    if m:
      result.extend(split_values(m.groupdict()["path"]))
    else:
      result.append(value)
  #print(result)
  return result


def get_content(path):
  return open(path).read()


def main(aliases_path):
  aliases_content = get_content(aliases_path)
  #print(aliases_content)
  cleaned_content = cleaned(aliases_content)
  #print(cleaned_content)
  result = []
  for key, values in split2kv(cleaned_content):
    values = split_values(values)
    for value in values:
      result.append((key, value))
  result.sort()
  __import__('pprint').pprint(result)
  return result
