import os
import pathlib

import dotenv

dotenv.load_dotenv()

# usually, this is mapped volume. but nothing stops you from pointing this to a folder on your local machine
INSTALL_DLCS_TO_PATH = pathlib.Path(__file__).parent / 'installed'
# this is a temporary folder to store downloaded files
TEMP_FOLDER_PATH = pathlib.Path(__file__).parent / 'temp'
# this is a folder where we store manifest.json file
SOURCES_TO_INSTALL_FROM_ENV = os.getenv('SOURCES_TO_INSTALL')

GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_USERNAME or not GITHUB_TOKEN:
    raise ValueError('You need to provide both GITHUB_USERNAME and GITHUB_TOKEN in .env file')


DLC_EXPECTED_STRUCTURE = {
    'manifest.json': 'file',
    'data': 'folder',
    'components': 'folder',
    'assets': 'folder',
    'functions': 'folder',
    'translations': 'folder',
    'LICENSE': 'file',
}
