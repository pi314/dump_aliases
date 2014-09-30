import sys

if len(sys.argv) < 3:
    print('Usage:')
    print(' ', sys.argv[0], '<etc_aliases> <name_files_dir>')
    exit()

ETC_ALIASES = sys.argv[1]
NAME_FILES_DIR = sys.argv[2]

