"""
Tool name: remove_logs
Description: Remove those pesky log folders that end up absolutely everywhere, especially after running tests.
Warning: Beware of any unrelated "log" folders you have created and wish to keep, as this tool will delete them too!
         Please run this script from the "tools" directory, otherwise it won't work.
"""

from shutil import rmtree
from glob import glob
from os import path

WARNING = '''
    Beware of any unrelated "log" folders you have created and wish to keep, as this tool will delete them too!
    Please run this script from the "tools" directory, otherwise it won't work.
    If you have acknowledged this information, please type 'OK': '''

def main():
    """
    Main
    """
    assert path.basename(path.abspath('.')) == 'tools', 'You must be in the \'tools\' directory to run this script!'
    assert 'logs' in [file[-4:] for file in glob("../**", recursive=True)], 'No log folder found.'
    if not input(f'Warning: {WARNING}').lower() == 'ok':
        return
    for file in glob("../**", recursive=True):
        if not file[-4:] == 'logs':
            continue
        rmtree(file)
        print(f'Deleted {file}')

if __name__ == '__main__':
    main()