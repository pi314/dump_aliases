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

db = {}

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

def add_to_db (list_name, data):
    global db

    data = data.strip()

    if list_name not in db:
        db[list_name] = set()

    db[list_name].add(data)

def process_record (record):
    list_name, record_type, data = record
    print(list_name, record_type, data)
    if record_type == 'file':
        pass
    elif record_type == 'mail':
        add_to_db(list_name, data)
    else:
        print('Error record type:', record)
        exit()

def dump_db ():
    for list_name in db:
        for data in db[list_name]:
            print( '{}:{}'.format(list_name, data) )

def main ():
    load_aliases_file()
    for i in aliases_file:
        process_record(i)
    dump_db()

if __name__ == '__main__':
    main()

