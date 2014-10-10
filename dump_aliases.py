r"""
usage:
  $cmd $aliases_file_path

background:
  - assume that the aliases file has passed ``postalias``

issues:
  - store all error/warning(s) and output it.

cleaning rules:
  1. '#.*$' should be ignored
  2. replace '\n |[\t\r\f\v]' as ' '
  3. '"[^"]"'should not be modified; else:
    a. ' +' -> ' '
    b. ' ?: ?' -> ':'
    c. ' ?, ?' -> ', '
  4. remove blank line

key verifying rules:
  1. '""' -> ' '
  2. '"([^"]+)"' -> \1
"""


import re


def cleaned(content):
  r"""
  >>> content = '\na  :  b  ,c:,  "  ,  \n  : d"\t\r\n\r e\n'
  >>> cleaned(content)
  'a:b, c:, ", :d" e\n'
  """
  def subclean(m):
    s = m.group()
    s = re.sub(r' +', ' ', s)
    s = re.sub(r' ?: ?', ':', s)
    s = re.sub(r' ?, ?', ', ', s)
    return s
  content = re.sub(r'#.*$', '', content, flags=re.M)
  content = re.sub(r'\n\s|[\t\r\f\v]', ' ', content)
  content = re.sub(r'(.*)("[^"]*")?', subclean, content)
  content = re.sub(r'^\s+', '', content)
  return content


def clean_key(key):
  r"""
  >>> cleaned_key('a \"b c\"\"\"d')
  'a b c d'
  """
  return re.sub(r'"([^"]*)"', lambda m: m.group(1) or ' ', key)


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
  for value in re.split(r"\s*(?:[,\n])\s*", values.strip()):
    m = re.match(r":include:\s*(?P<path>.*)", value)
    if m:
      subcontent = get_content(m.groupdict()["path"])
      result.extend(split_values(cleaned(subcontent)))
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
  #__import__('pprint').pprint(result)
  return result


if __name__=='__main__':

  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('aliases_path')
  aliases_path = parser.parse_args().aliases_path
  print(main(aliases_path))
