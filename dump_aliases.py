import sys
import os
import re

ETC_ALIASES = ''
NAME_FILES_DIR = ''

FILE = 'file'
MAIL = 'mail'

aliases_file = []
list_relation = {}
file_table = {}
db = {}

def load_aliases_file ():
    '''
        Load ETC_ALIASES file and parse it in ``aliases_file`` variable
        format:
            (list_name, record_type, data)
            list_name: (string) the name of mailing list
            record_type: (string) "file" or "mail"
            data: (string) an email address or a file name
    '''
    global aliases_file

    for i in open(ETC_ALIASES):
        i = re.sub(r'#.*$', '', i).strip()
        if i == '' or i[0] == '#':
            continue

        if ':include:' in i:
            l = i.split(':')
            list_name, record_type, name_file = l[0], FILE, l[-1].split('/')[-1].strip()
            aliases_file.append( (list_name, record_type, name_file) )
            file_table[name_file] = list_name

        else:
            l = i.split(':')
            list_name = l[0]
            emails = l[-1].split(',')
            for j in emails:
                aliases_file.append( (list_name, MAIL, j.strip()) )

def setup_list_relation ():
    '''
        Set up the relation between mailing lists
        type(list_relation) == dict
        for i in list_relation: type(i) == set
    '''
    global list_relation

    for i in aliases_file:
        list_relation[ i[0] ] = set()

def add_to_db (list_name, data):
    '''
        ``db`` is a dictionary
        list -> email address
    '''
    global db
    data = data.strip()

    if list_name not in db:
        db[list_name] = set()

    db[list_name].add(data)

def process_name_file (list_name, file_name, stack):
    if file_name in stack: return
    full_file_name = '/'.join( [NAME_FILES_DIR, file_name] )

    for i in open(full_file_name):
        i = re.sub(r'#.*$', '', i).strip()
        if i == '' or i[0] == '#':
            continue

        if ':include:' in i:
            sub_file_name = i.split('/')[-1]
            if sub_file_name in file_table:
                list_relation[list_name].add( file_table[sub_file_name] )
            process_name_file(list_name, sub_file_name, stack + [file_name])

        elif '@' in i:
            add_to_db(list_name, i)

        elif i in list_relation:
            list_relation[list_name].add(i)

        else:
            add_to_db(list_name, i)

def process_list_record (record):
    global file_table

    list_name, record_type, data = record

    if record_type == FILE:
        process_name_file(list_name, data, [])

    elif record_type == MAIL:
        add_to_db(list_name, data)

    else:
        print('Error record type:', record)
        exit()

def dump_db ():
    for list_name in db:
        for data in db[list_name]:
            print( '{}:{}'.format(list_name, data) )

def clean_list_relation ():
    global list_relation

    ret = {}
    for i in list_relation:
        if list_relation[i] != set():
            ret[i] = list_relation[i]

    list_relation = ret

def apply_relations (main_list_name, stack):
    if main_list_name in stack: return

    if main_list_name not in db:
        # this file is empty, or everything was commented
        return set()

    ret = db[main_list_name]

    if main_list_name not in list_relation:
        return ret

    for sub_list_name in list_relation[main_list_name]:
        ret |= apply_relations(sub_list_name, stack + [main_list_name])

    return ret

def main ():
    global ETC_ALIASES
    global NAME_FILES_DIR

    if len(sys.argv) < 3:
        print('Usage:')
        print(' ', sys.argv[0], '[etc-aliases-file] [name-files-dir]')
        exit()

    ETC_ALIASES    = sys.argv[1]
    NAME_FILES_DIR = sys.argv[2]

    load_aliases_file()
    setup_list_relation()

    for i in aliases_file:
        process_list_record(i)

    clean_list_relation()

    for i in db:
        db[i] |= apply_relations(i, [])

    dump_db()

    for i in list_relation:
        for j in list_relation[i]:
            print('#', '{}:{}'.format(i, j) )

if __name__ == '__main__':
    main()

