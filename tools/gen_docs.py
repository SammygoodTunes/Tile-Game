"""
Tool name: gen_docs
Description: Automatically generate the RST files in docs.
Warning: This will potentially not work with PyInstaller.
"""

from glob import glob
from os import mkdir, remove
from os.path import join, exists
import pkgutil
import game

DOC_PATH = join('..', join('docs', 'game'))
RST_EXT = '.rst'

def main():
    """
    Main
    """
    if not exists(DOC_PATH):
        print(f'Creating path \'{DOC_PATH}\' as it does not exist.')
        mkdir(DOC_PATH)

    for file in glob(join(DOC_PATH, "*" + RST_EXT)):
        remove(file)

    modules = {}

    for module in pkgutil.walk_packages(game.__path__, game.__name__ + '.'):
        namespaces = module.name.count('.')
        if namespaces == 1:
            modules[module.name.split('.')[1]] = []
        elif namespaces == 2:
            modules[module.name.split('.')[1]].append(module.name.split('.')[2])
        elif namespaces == 3:
            modules[module.name.split('.')[1]].append(module.name.split('.')[2] + '.' + module.name.split('.')[3])

    for module in modules:
        with open(join(DOC_PATH, module + RST_EXT), 'w') as rst:
            print(f'Generating rst for module `{module}` ({join(DOC_PATH, module + RST_EXT)})')
            module_title = f'`{module}` module'
            rst.write(f'\n{module_title}\n' + '=' * len(module_title))
            rst.write(f'\n.. automodule:: game.{module}\n   :members:\n   :undoc-members:\n')
            for submodule in modules[module]:
                namespaces = submodule.count('.')
                print(f"{'  >>' if namespaces else ' >'} "
                      f"Generating rst for submodule `{submodule}` ({join(DOC_PATH, module + RST_EXT)})")
                submodule_title = f'`{module}.{submodule}`'
                rst.write(f'\n{submodule_title}\n' + ('-' if not namespaces else '_') * len(submodule_title))
                rst.write(f'\n.. automodule:: game.{submodule}\n   :members:\n   :undoc-members:\n')
    print(f'Done! (Generated {len(glob(join(DOC_PATH, "*" + RST_EXT)))} file(s))')

if __name__ == '__main__':
    main()
