r"""
usage:
  $cmd $aliases_file_path

background:
  - assume that the aliases file has passed ``postalias``

issues:
  - store all error/warning(s) and output it.
  - consider '\"'

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


def get_cleaned_content(file_path):
  """
  file_path: str -> cleaned lines: list
  """
  def cleaned(content):
    r"""
    >>> content = '\na  :  b  ,c:,  "  ,  \n  : d"\t\r\n\r e\n'
    >>> cleaned(content)
    'a:b, c:, ", :d" e\n'
    """
    def subclean(m):
      s = m.group(1)
      s = re.sub(r' +', ' ', s)
      s = re.sub(r' ?: ?', ':', s)
      s = re.sub(r' ?, ?', ', ', s)
      return s
    content = re.sub(r'#.*$', '', content, flags=re.M)
    content = re.sub(r'\n\s|[\t\r\f\v]', ' ', content)
    content = re.sub(r'(.*)(".*?(?<!\\)")?', subclean, content)
    content = re.sub(r'^\s+', '', content)
    return content

  return cleaned(open(file_path).read()).splitlines()


def clean_key(key):
  r"""
  >>> clean_key('a \"b c\"\"\"d')
  'a b c d'
  """
  return re.sub(r'"([^"]*)"', lambda m: m.group(1) or ' ', key)


def split_values(values):
  """
  cleaned values: str -> list
  >>> split_values('b, c:, ", :d" e, :include:/dev/null')
  ['b', 'c:', '", :d"', 'e']
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
