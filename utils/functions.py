import sys
import datetime
from datetime import timedelta


# FUNCTIONS **********************************************
# All functions that are not commands or direct DB functions
# should go in this file, and imported into the neccessary
# cog




# Get functions
#-------------------------

def GetQueryValues(args):
    # define the dictionary of querys to return
    result = {
        "query": {
            "username": None,
            "active": None,
            "userNickname": None,
            "gamertag": None,
            "sortBy": None
        },
        "error": {
            "errorMessage": None
        }
    }

    for arg in args:
        if arg.lower() == 'active':
            result["query"]["active"] = True

        elif arg.lower() == 'inactive':
            result["query"]["active"] = False

        elif arg.lower().split('=')[0] == 'name' or arg.lower().split('=')[0] == 'username':
            result["query"]["username"] = "'{}'".format(arg.split('=')[1])

        elif arg.lower().split('=')[0] == 'nickname' or arg.lower().split('=')[0] == 'userNickname':
            result["query"]["userNickname"] = "'{}'".format(arg.split('=')[1])

        elif arg.lower().split('=')[0] == 'gamertag':
            result["query"]["gamertag"] = "'{}'".format(arg.split('=')[1])

        # Below we handle all the sortBy optionsa user could input
        elif arg.lower().split('=')[0] == 'sortby':

            # inactive and date are options, but are not the name of the db tables column, so special if conditions for them
            if arg.lower().split('=')[1] == 'inactive':
                result["query"]["sortBy"] = 'active ASC'

            elif arg.lower().split('=')[1] == 'date':
                result["query"]["sortBy"] = 'statusChanged DESC'

            # for the rest of the sortBy options, 1 to 1 with db table column name, just loop through our dict
            else:
                for key in result["query"]:
                    if arg.lower().split('=')[1] == key.lower():
                        result["query"]["sortBy"] = '{} DESC'.format(arg.split('=')[1])
                        break
                
                if not result["query"]["sortBy"]:
                    result["error"]["errorMessage"] = 'ERROR for sortBy value. "sortBy value must be either "date", "username", "active", "inactive", userNickname", or "gamertag"'
                    return result 

        # If you get here, then no argument matched the allowed options, so we have an error
        else:
            result["error"]["errorMessage"] = 'ERROR at param {}. Either the paramater was not understood or the value "{}" is invalid'.format(arg.split('=')[0], arg.split('=')[1])
            return result

    #finally return the result
    return result



def GetMemberListRow(memberRow):
    output = ''

    # use nickname if one exists, otherwise default to username
    print(memberRow)
    nameOutput = memberRow[5] if memberRow[5] else memberRow[0]

    # prepare output string
    output += '`{}{}`'.format(nameOutput, '.' * (17 - len(nameOutput)))
    # output += ' `{}{}` '.format(memberRow[3] if memberRow[3] else '', '.' * (13 - len(memberRow[3])) if memberRow[3] else '.' * 13)
    output += ' {} '.format( ':slight_smile:' if memberRow[4] else ':sob:')
    date = memberRow[2].split('T')[0].split('-')
    output += ' `..{}/{}/{}`\n'.format(date[1], date[2], date[0][2::])

    return output