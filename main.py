import settings 

import src
import scripts.output_local_folders as scripts

if __name__ == '__main__':
    if settings.DLC_MOVEMENT_STRATEGY == 'local':
        scripts.output_local_folders()
        if not settings.IGNORE_LOCAL_STRATEGY_CONFIRMATION:
            print('Are you sure you want to proceed with local strategy?')
            confirmation = input('Type "yes" to proceed: ')
            if confirmation.lower() != 'yes':
                print('Exiting...')
                exit(0)

    src.start()
