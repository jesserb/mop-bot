# use the functions here to load arguments fromt he config file
import sys
from utils.db import GetBotConfigs,  AuthorizeDeveloper, IsBotOwner


# Returns true if this is the bot owner
def AuthorizeUser():
    isBotOwner = False

    # a sub function to take in user auth, and create session
    def AuthorizeAndWriteDevsession():
        success = False
        while not success:
            username = input('Enter Discord Username: ')
            pin = input('Enter 4 digit pin: ')
            success = AuthorizeDeveloper(username, pin)
            if not success:
                print('\nCredentials incorrect.. Please try again or contact Bop...')
        
        devsession = open('devsession', 'w')
        devsession.write('username: {}\npin: {}'.format(username, pin))
        isBotOwner = IsBotOwner(username, pin)
        devsession.close()
        return isBotOwner
    try:
        authfile = open('devsession')
        auth = authfile.readlines()
        username = auth[0].split()[1].split('\n')[0]
        pin = auth[1].split()[1].split('\n')[0]
        success = AuthorizeDeveloper(username, pin)
        if success:
            isBotOwner = IsBotOwner(username, pin)
            print('\nAuthenticated... Access Granted')
        else:
            print('\nAuthentication failed.. devsession no longer valid')
            isBotOwner = AuthorizeAndWriteDevsession()
    except:
        print('\nNo "devsession" found - authorization required...')
        isBotOwner = AuthorizeAndWriteDevsession()

    return isBotOwner



# Based on the system arguments given, loads the correct bot
def loadBotConfigs():

    botType = ''
    # error checking
    if len(sys.argv) > 2:
        print('**ERROR: Too many arguments. program takes at most one.\nexiting... ... ...')
        sys.exit()
        
    # handle argument
    if len(sys.argv) > 1:
        botType = sys.argv[1]
    else:
        botType = 'Mop'

    # Load configs
    configs = GetBotConfigs(botType)
    isBotOwner = AuthorizeUser()

    if not isBotOwner and len(sys.argv) == 1:
        print('\n**ERROR: NO TEST ENVIRONMENT IN STARTUP COMMAND!**')
        print('Only the Bot owner can run the `startup.py` without an argument, as this starts up **PROD**.')
        print('Retry command with a testsim argument.. ... ...\n')
        sys.exit()

    return {
        "token": configs[1],
        "prefix": configs[3]
    }
    