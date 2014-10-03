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
list_relation = {}
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

def setup_list_relation ():
    global list_relation

    for i in aliases_file:
        list_relation[ i[0] ] = set()

def add_to_db (list_name, data):
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
            process_name_file(list_name, sub_file_name, stack + [file_name])
        elif '@' in i:
            add_to_db(list_name, i)
        elif i in list_relation:
            list_relation[list_name].add(i)
            pass
        else:
            add_to_db(list_name, i)

def process_list_record (record):
    list_name, record_type, data = record

    if record_type == 'file':
        process_name_file(list_name, data, [])
    elif record_type == 'mail':
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

def merge_relations (list_name=None, stack=[]):
    global list_relation

    if list_name in stack: return set()

    if list_name == None:
        # merge first layer
        for i in list_relation:
            list_relation[i] = merge_relations(i, [])

    else:
        # merge specific list
        ret = set()
        for i in list_relation[list_name]:
            if i in list_relation:
                ret |= merge_relations(i, stack+[list_name])

            else:
                ret.add(i)

        list_relation[list_name] = ret
        return list_relation[list_name]

def main ():
    load_aliases_file()
    setup_list_relation()

    for i in aliases_file:
        process_list_record(i)

    clean_list_relation()

    # merge lists accroding to list_relation
    merge_relations()

    dump_db()

if __name__ == '__main__':
    main()

