from src.package_manager import PackageManager


def start():
    print('Starting installation')
    manager = PackageManager()
    manager.initialize_installation()
    print('Installation finished')
