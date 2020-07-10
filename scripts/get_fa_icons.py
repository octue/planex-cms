""" Use:

$ python get_fa_icons.py > fa_icons.py

to create a python module listing all the fa icons

"""
from os import remove, walk, path
from pprint import PrettyPrinter
from requests import get
from shutil import rmtree
from zipfile import ZipFile

# Font awesome release
RELEASE = '5.13.0'
release_name = 'Font-Awesome-{}'.format(RELEASE)
zip_file_name = '{release_name}.zip'.format(release_name=release_name)

# Ensure cleanup is done even if there's an exception
try:

    # Download the release
    url = 'https://github.com/FortAwesome/Font-Awesome/archive/{}.zip'.format(RELEASE)
    r = get(url, allow_redirects=True)
    with open(zip_file_name, 'wb') as f:
        f.write(r.content)

    # Extract all the contents of zip file into the release directory
    with ZipFile(zip_file_name, 'r') as zipObj:
        zipObj.extractall()

    # Cycle through the SVG subdirectories to get lists of all the classes
    icons = {}
    for group in walk('./{}/svgs/'.format(release_name)):
        group_name = path.split(group[0])[-1]
        if group_name not in ['', '.', '..']:
            group_class = 'fa{}'.format(group_name[0])
            icons[group_class] = []
            for icon in group[2]:
                icon_name = icon.replace('.svg', '')
                icon_class = 'fa-{}'.format(icon_name)
                icons[group_class].append(icon_class)

    pp = PrettyPrinter(indent=4)
    print('fa_icons = {}'.format(pp.pformat(icons)))

except Exception as e:
    raise

finally:
    rmtree(release_name)
    remove(zip_file_name)
