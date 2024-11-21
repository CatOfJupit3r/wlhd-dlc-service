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

# this is a strategy that we use to move DLCs
# If it is dockerfile, then it assumes that you will have mapped volume to INSTALL_DLCS_TO_PATH
# Else, it will copy DLCs to designated folders on the local machine
DLC_MOVEMENT_STRATEGY = os.getenv('DLC_MOVEMENT_STRATEGY', 'dockerfile')
IGNORE_LOCAL_STRATEGY_CONFIRMATION = os.getenv('IGNORE_LOCAL_STRATEGY_CONFIRMATION', 'false').lower() == 'true'

LOCAL_STRATEGY_FOLDERS = []
if DLC_MOVEMENT_STRATEGY == 'local':
    # This should be personalized according to your folder setup
    # Provided values are how I, the creator, have it set up
    # WARNING: THIS WILL RESULT IN LOSS OF DATA IF SET UP INCORRECTLY
    # You can check the paths by running the following command in the terminal:
    LOCAL_STRATEGY_FOLDERS = [
        # coordinator
        pathlib.Path(__file__).parent.parent / 'coordinator-server' / 'src' / 'installed',
        # game engine
        pathlib.Path(__file__).parent.parent / 'game-server' / 'installed',
        # cdn
        pathlib.Path(__file__).parent.parent / 'wlhd-cdn-service' / 'data' / 'installed',
    ]

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
