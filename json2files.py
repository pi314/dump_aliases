"""
1. This program now will set the name of test files' folder
   be "test_files".
2. The design of command line might be improved in the future.
3. If there already exists "test_files" file or folder, it
   would rename it with suffix "\.%d"....this feature might
   be implement in the future.
4. Check if suffix of filename of import file is ".json".
"""


from os import mkdir
from os.path import join as path_join


def gen_files(root_path, data):
  
  def list2file(filename, data):
    with open(filename, 'w') as f:
      for line in data:
        f.write(line.format(root_path=root_path)+'\n')

  def dict2dir(dirname, data):
    mkdir(dirname)
    for name in data:
      if type(data[name]) is list:
        list2file(path_join(dirname, name), data[name])
      else:
        dict2dir(path_join(dirname, name), data[name])

  dict2dir(root_path, data)


if __name__=='__main__':

  from argparse import ArgumentParser
  from sys import stderr
  from os.path import abspath
  from json import load as load_json

  parser = ArgumentParser()
  parser.add_argument('json_file')
  json_file = parser.parse_args().json_file
  
  root_path = abspath(json_file.rsplit('.',1)[0])
  data = load_json(open(json_file))

  try:
    gen_files(root_path=root_path, data=data)
  except:
    stderr.write("....generate test files failed >.<|||\n")
    stderr.write("....maybe \"test_files\" already exists?\n")
  else:
    stderr.write("....generate test files successfully\n")
