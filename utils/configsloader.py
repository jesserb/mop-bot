# use the functions here to load arguments fromt he config file
import sys

def loadDBFromConfigs():
    # handle argument
    if len(sys.argv) > 1:
        botType = sys.argv[1]
    else:
        botType = 'Mop'


    # Load configs
    configFile = open('config')
    configs = configFile.readlines()
    config = {
        'Mop': {
            'db': (configs[4].split()[1]).split('\n')[0]
        },
        'MopTestSim': {
            'db': (configs[10].split()[1]).split('\n')[0]
        },
    }

    return './utils/{}'.format(config[botType]['db'])