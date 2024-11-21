import settings


def output_local_folders():
    print(f'LOCAL_STRATEGY_FOLDERS = {settings.LOCAL_STRATEGY_FOLDERS}')
    for folder in settings.LOCAL_STRATEGY_FOLDERS:
        print('FOLDER PATH:', folder)
        print(f'Does folder {folder.name} exists: {folder.exists()}')
        if folder.exists():
            print(f'Files in {folder.name}: {list(folder.iterdir())}')
        print()


if __name__ == '__main__':
    output_local_folders()
