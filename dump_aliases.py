import sys
import os
import re

if len(sys.argv) < 3:
    print('Usage:')
    print(' ', sys.argv[0], '<etc_aliases> <name_files_dir>')
    exit()

ETC_ALIASES = sys.argv[1]
NAME_FILES_DIR = sys.argv[2]

aliases_file = []

def load_aliases_file ():
    global aliases_file
    for i in open(ETC_ALIASES):
        i = re.sub(r'#.*$', '', i).strip()
        if i == '' or i[0] == '#':
            continue
        if ':include:' in i:
            l = i.split(':')
            list_name, record_type, name_file = l[0], 'file', l[-1].split('/')[-1]
            aliases_file.append( (list_name, record_type, name_file) )
        else:
            l = i.split(':')
            list_name = l[0]
            emails = l[-1].split(',')
            for j in emails:
                aliases_file.append( (list_name, 'mail', j.strip()) )

def main ():
    load_aliases_file()
    for i in aliases_file:
        print(i)

if __name__ == '__main__':
    main()

