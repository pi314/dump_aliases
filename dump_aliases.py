r"""
usage:
  $cmd $aliases_file_path

background:
  - assume that the aliases file has passed ``postalias``

issues:
  - store all error/warning(s) and output it.

cleaning rules:
  1. r'#.*$' should be ignored
  2. replace r'\n |[\t\r\f\v]' as ' '
  3. r'".*?(?<!\\)"'should not be modified; else:
    a. r' +' -> ' '
    b. r' ?: ?' -> ':'
    c. r' ?, ?' -> ', '
  4. remove blank line

key verifying rules:
  1. r'""' -> ' '
  2. r'"([^"]+)"' -> '\1'

doctest:
  >>> content = '''
  ... a \"b c\"\"\"d:  b  ,c:,  "  , \x20
  ...   : \\"d"\t\r
  ... \r e
  ... f:g
  ... '''
  >>> records = cleaned(content).splitlines()
  >>> records == ['a \"b c\"\"\"d:b, c:, "  ,    : \\"d" e', 'f:g']
  True
  >>> alias = records[0]
  >>> alias == 'a \"b c\"\"\"d:b, c:, "  ,    : \\"d" e'
  True
  >>> split_alias(alias) == ('a b c d', ['b','c:','"  ,    : \\"d"','e'])
  True
"""


import re


def cleaned(content):
  """
  Accoring to ``postalias`` progress and binary data in aliases.db,
  rewritting it.
  """
  def subclean(m):
    s, t = m.groups()
    s = re.sub(r' +', ' ', s)
    s = re.sub(r' ?: ?', ':', s)
    s = re.sub(r' ?, ?', ', ', s)
    t = t or ''
    return s + t
  content = re.sub(r'#.*$', '', content, flags=re.M)
  content = re.sub(r'\n\s|[\t\r\f\v]', ' ', content)
  content = re.sub(r'([^"]*)(".*?(?<!\\)")?', subclean, content)
  content = re.sub(r'^\s+', '', content)
  return content


def clean_key(key):
  """
  key: str -> cleaned key: str
  """
  return re.sub(r'"([^"]*)"', lambda m: m.group(1) or ' ', key)


def split_values(values):
  """
  cleaned values: str -> list
  """
  result = []
  for value in re.findall(r'".*?(?<!\\)"|[^, ]+', values):
    if value.startswith(':include:'):
      cleaned = get_cleaned_content(value[9:])
      result.extend(split_values(' '.join(cleaned)))
    else:
      result.append(value)
  return result


def split_alias(record):
  """
  "key:values" -> (key, values)
  """
  key, values = record.split(':', 1)
  return clean_key(key), split_values(values)


def get_cleaned_content(file_path):
  """
  file_path: str -> cleaned lines: list
  """
  return cleaned(open(file_path).read()).splitlines()


def parse_include_file(file_path):
  """
  _ -> values: [value]
  """
  return split_values(get_cleaned_include_file(file_path))


def parse_aliases_file(aliases_path):
  """
  _ -> aliases: {key: [value]}
  """
  aliases = get_cleaned_content(aliases_path)
  return {k:vs for k,vs in map(split_alias, aliases)}


if __name__=='__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('aliases_path')
  aliases_path = parser.parse_args().aliases_path

  parsed_data = parse_aliases_file(aliases_path)
  for k,v in sorted(
    ((k,v) for k,vs in parsed_data.items() for v in vs),
    key=lambda t:t
    ):
    print("%s:%s"%(k,v))
