import json
import os
import traceback
from pathlib import Path
from typing import List

from git import Repo

import settings
from .utils import link_is_valid, purge, copy, inject_github_token


class PackageManager:
    _installed_packages: List[str]  # list of installed packages
    _packages_to_install: List[str]  # list of sources from env

    def __init__(self):
        self._installed_packages = []
        self._packages_to_install = []

    def _reset(self) -> 'PackageManager':
        """
        Resets the PackageManager
        """
        self._installed_packages = []
        self._packages_to_install = []
        return self

    def initialize_installation(self) -> None:
        """
        Initializes installation process
        """

        """ PREPARATION STEP """
        self._reset()
        self._process_packages_from_env()
        self._purge_dirs()
        self._verify_dirs()

        """ INSTALLATION STEP """
        self._populate_installation_folder()

        """ VERIFICATION STEP """
        self._purge_dirs()

    def _process_packages_from_env(self) -> None:
        """
        Processes packages from environment variable
        """
        if settings.SOURCES_TO_INSTALL_FROM_ENV is None:
            raise ValueError('Environment variable SOURCES_TO_INSTALL is not set')
        # sources from env are declared in for of string `link1,link2,link3`
        packages_to_install = settings.SOURCES_TO_INSTALL_FROM_ENV.split(',')
        if not packages_to_install:
            raise ValueError('No packages to install')
        for package in packages_to_install:
            package = package.strip()
            if link_is_valid(package):
                self._packages_to_install.append(package)
            else:
                raise ValueError(f'Invalid link: {package}')
        if not self._packages_to_install:
            raise ValueError('No valid links to install found')

    @staticmethod
    def _install_package_to_temp(package_url: str) -> Path:
        """
        Installs package to temporary folder
        """
        dlc_folder_name = package_url.split('/')[-1]
        if dlc_folder_name.endswith('.git'):
            dlc_folder_name = dlc_folder_name[:-4]
        temp_folder_path = settings.TEMP_FOLDER_PATH / dlc_folder_name
        if temp_folder_path.exists():
            print(f'Deleting {temp_folder_path}')
            purge(temp_folder_path)
        os.makedirs(temp_folder_path)
        Repo.clone_from(inject_github_token(package_url), temp_folder_path)
        return temp_folder_path

    def _verify_installed_package(self, package_path: Path) -> None:
        """
        Verifies if package is installed
        """
        self._verify_manifest(package_path)

        for key, value in settings.DLC_EXPECTED_STRUCTURE.items():
            match value:
                case 'file':
                    if not (package_path / key).exists():
                        raise FileNotFoundError(f'File {key} not found in {package_path}')
                case 'folder':
                    if not (package_path / key).is_dir():
                        raise FileNotFoundError(f'Folder {key} not found in {package_path}')
                case _:
                    raise ValueError(f'Invalid value {value} for key {key}')

    @staticmethod
    def _rename_dlc_to_proper_name(package_path: Path) -> Path:
        """
        Renames package to a proper name from manifest.json
        """
        manifest_path = package_path / 'manifest.json'
        if not manifest_path.exists():
            raise FileNotFoundError(f'Manifest not found in {package_path}')
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
            proper_name = manifest.get('descriptor')
            if not proper_name:
                raise ValueError(f'Proper name not found in {manifest_path}')
        proper_package_path = settings.TEMP_FOLDER_PATH / proper_name
        if proper_package_path.exists():
            print(f'Package "{proper_package_path.name}" already exists in installed. Deleting...')
            purge(proper_package_path)
        package_path.rename(proper_package_path)
        return proper_package_path

    @staticmethod
    def _move_temp_dlc_to_mapped_volume_folder(package_path: Path) -> None:
        """
        Renames package from temporary folder to a proper name from manifest.json
        """
        proper_package_path = settings.INSTALL_DLCS_TO_PATH / package_path.name
        if proper_package_path.exists():
            print(f'Package "{proper_package_path.name}" already exists in installed. Deleting...')
            purge(proper_package_path)
        package_path.rename(proper_package_path)

    @staticmethod
    def _move_temp_dlc_to_local_folders(package_path: Path) -> None:
        """
        Moves DLCs to local folders
        """
        for folder in settings.LOCAL_STRATEGY_FOLDERS:
            if not folder.exists():
                print(f'Folder {folder.name} does not exist. Creating...')
                folder.mkdir()
            proper_package_path = folder / package_path.name
            if proper_package_path.exists():
                print(f'Package "{proper_package_path.name}" already exists in {folder}. Deleting...')
                purge(proper_package_path)
            copy(package_path, proper_package_path)
            print(f'Moved {proper_package_path.name} to {folder}')
        purge(package_path) # remove temp folder

    @staticmethod
    def _clear_dlc_folder(package_path: Path) -> None:
        """
        Clears DLC folder from unnecessary files and folders
        """
        expected_names = settings.DLC_EXPECTED_STRUCTURE.keys()
        for item in package_path.iterdir():
            if item.name not in expected_names:
                print(f'Deleting {item}')
                purge(item)

    @staticmethod
    def _verify_dirs():
        """
        Checks if installation folder exists and creates it if it does not
        """
        required_folders = [settings.INSTALL_DLCS_TO_PATH, settings.TEMP_FOLDER_PATH]
        print(f'Verifying folders...')
        for folder in required_folders:
            if not folder.exists():
                print(f'Folder {folder.name}. Creating folder...')
                folder.mkdir()
        print(f'Verification finished')

    @staticmethod
    def _purge_dirs() -> None:
        print(f'Purging folders...')
        folders_to_purge = [settings.TEMP_FOLDER_PATH]
        for folder in folders_to_purge:
            print(f'Purging folder {folder.name}...')
            purge(folder)
        print(f'Purging finished')

    def _populate_installation_folder(self) -> None:
        """
        If folder is fresh, it will download all packages source provided by API server (mainly GitHub)
        After that, we should clean the folder from unnecessary files and folders (README, .git, etc.)
        """
        if not self._packages_to_install:
            raise ValueError('No packages to install')
        for dlc in self._packages_to_install:
            try:
                print(f'Installing new dlc from "{dlc}"...')
                temp_package_path = self._install_package_to_temp(dlc)
                self._verify_installed_package(temp_package_path)
                proper_package_path = self._rename_dlc_to_proper_name(temp_package_path)
                self._clear_dlc_folder(proper_package_path)

                if settings.DLC_MOVEMENT_STRATEGY == 'local':
                    self._move_temp_dlc_to_local_folders(proper_package_path)
                elif settings.DLC_MOVEMENT_STRATEGY == 'dockerfile':
                    self._move_temp_dlc_to_mapped_volume_folder(proper_package_path)
                else:
                    raise ValueError(f'Invalid DLC_MOVEMENT_STRATEGY: {settings.DLC_MOVEMENT_STRATEGY}')

                print(f'DLC {proper_package_path.name} installed successfully')
            except Exception as e:
                print(f'Error during installation of {dlc}: {e}')
                traceback.print_exc()
                continue

    @staticmethod
    def _verify_manifest(package_path: Path) -> None:
        """
        Verifies if installed package has a manifest.json file
        """
        manifest_path = package_path / 'manifest.json'
        if not manifest_path.exists():
            raise FileNotFoundError(f'Manifest not found in {package_path}')
        manifest = json.load(open(manifest_path, 'r'))
        if not manifest.get('descriptor'):
            raise ValueError(f'Descriptor not found in {manifest_path}')
