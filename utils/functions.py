import sys
import datetime
from datetime import timedelta
from zipfile import ZipFile
import shutil
import os


# FUNCTIONS **********************************************
# All functions that are not commands or direct DB functions
# should go in this file, and imported into the neccessary
# cog



# Get functions
#-------------------------

def GetMention(id):
    return '<@{}>'.format(id)

def GetDiscordMemberObject(members, memberID):
    for member in members:
        if int(member.id) == int(memberID):
            return member
    return None

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
    nameOutput = memberRow[5] if memberRow[5] else memberRow[0]

    # prepare output string
    output += '`{}{}`'.format(nameOutput, '.' * (17 - len(nameOutput)))
    # output += ' `{}{}` '.format(memberRow[3] if memberRow[3] else '', '.' * (13 - len(memberRow[3])) if memberRow[3] else '.' * 13)
    output += ' {} '.format( ':slight_smile:' if memberRow[4] else ':sob:')
    date = memberRow[2].split('T')[0].split('-')
    output += ' `..{}/{}/{}`\n'.format(date[1], date[2], date[0][2::])

    return output


def PrepareHiddenFiles():
    # change name of prod db to test db
    shutil.copy('./utils/mop.db', './utils/moptest1.db')
    sys.exit()

     # Create a ZipFile Object
    with ZipFile('hiddenfiles.zip', 'w') as zipObj:
        # Add multiple files to the zip
        zipObj.write('./utils/moptest1.db')
        zipObj.write('./utils/db.py')


def PrepareCollaboratorWelcomePackage(newCollaborator, pin):
    # Create a ZipFile Object
    content = CreateWelcomeTextFileForNewCollaborator(newCollaborator, pin)
    welcomeFile = open('./utils/PLEASE_READ', 'w')
    welcomeFile.write(content)
    welcomeFile.close()

    # change name of prod db to test db
    shutil.copy('./utils/mop.db', './utils/moptest1.db')
    sys.exit()
    with ZipFile('devWelcomePkg.zip', 'w') as zipObj:
        # Add multiple files to the zip
        zipObj.write('./utils/moptest1.db')
        zipObj.write('./utils/db.py')
        zipObj.write('./utils/PLEASE_READ')


# May have to find a better place for this eventually..... do not like this
def CreateWelcomeTextFileForNewCollaborator(username, pin):
    content = 'MOP BOT DEVELOPMENT\n———————————-/——-------\nWelcome package!\n\n\n\n\n'
    content += '--credentials--\nUsername: {}\ndev pin: {}\n\n\nSection I\nINTRO\n'.format(username, pin)
    content += '———-------------------------------------\n\n'
    content += 'Below is some information on how to get started on setting up your machine for running\nthe bot and development.\n\n'
    content += 'Below are two versions describing how to get started. The first is for experienced developers,\n'
    content += 'and the second is for those who may be completely new to development.\n\n\n\n'
    content += 'Section II\nSETUP & GETTING STARTED - experienced\n————————————————————---------------------\n\nClone the repository\n\n'
    content += '- Send your GitHub username to Bop so he can add you to the repository as\n'
    content += '  a collaborator. Then navigate to https://github.com/jesserb/mop-bot to clone\n'
    content += '  the repository. \n- The two files included in this welcome package should be added to the ./utils directory.\n'
    content += '- Make sure you install Python3.8 if you have not done so already.\n'
    content += '- install the discord.py rewrite library. Below are some examples of the install process,\n'
    content += '  assuming python3.8 has no special path settings for you (e.g setting it so using python3\n'
    content += '  auto calls python3.8):\n\n'
    content += '    # Linux/macOS\n'
    content += '    python3.8 -m pip install -U discord.py\n\n'
    content += '    # Windows\n'
    content += '    py -3.8 -m pip install -U discord.py\n\n'
    content += '- It is recommended that you use the IDE vscode for python development, and SQLiteStudio IDE\n'
    content += '  for dB manipulation. But feel free to go with whatever preference you have. \n'
    content += '- start up the bot locally by navigating to the root directory and typing the command: \n\n'        
    content += '    python3.8 startup.py MopTestSim1\n\n'
    content += 'Where MopTestSim1 should be any of the testing bots not currently in use. A testing bot\n'
    content += 'Will be created for each collaborator, so if there are 4 collaborators there would be\n4 testing bots.\n\n'
    content += '- when you first run the bot you will be promoted to enter your discord username and the\n'
    content += '  pin you set when you were invited as a collaborator (top of this file). This will create\n'
    content += '  a session file to authenticate you as a developer for all future project runs. If the\n'
    content += "  Session file is changed and/or deleted for any reason that's ok, you will have to manually\n"
    content += '  Re-authenticate on program run again and the session file will be created once more.\n\n\n\n\n'
    content += 'Section III\nSETUP & GETTING STARTED - beginner\n————————————————————------------------------\n\n'
    content += 'So welcome to your first bot! Below we will go through the steps above but in more detail. Note\n'
    content += 'That it is highly recommended to talk with Bop throughout this process for additional information\nAnd trouble shooting.\n\n'
    content += 'The Mop bot is built using python, but specifically the discord.py library, which essentially is a\n'
    content += 'Coding package which allows one to communicate with the Discord API using a pre-built python wrapper.\n'
    content += 'An API if you do not know, is simply a service one communicates to in order to receive data. For \n'
    content += 'Example on a website when logging in, one typically communicates with a login api - you type\n'
    content += 'A username, a password, and hit login, that information is then passed to an API "somewhere" who takes\n'
    content += 'That info, checks it with some sort of database, does a look up for you, and returns a session unique to\n'
    content += 'you.\n\nTo get started we will need to install a few things on your computer. Note I (Bop) am on Mac, so for you\n'
    content += "Windows users some of these steps may require some googling if they don't work!:\n\n"
    content += '1) python 3.8: https://www.python.org/downloads/\n'
    content += '   Above is a link to download python for your operating system. Install the package!\n\n'
    content += '2) git: https://git-scm.com/downloads\n'
    content += '   Git is how you get the code! The code lives on what is called a "repository". Feel\n'
    content += '   Free to look it up for more info, but basically it gives us a way to store code on the\n'
    content += '   Web, that way if you develop something new, you can "push" the new stuff to the repository\n'
    content += '   And I can "pull" your changes - so we stay in sync!\n\n'
    content += '3) discord.py - for this one simply open your terminal and copy and paste one of the following\n'
    content += '   Commands depending on your OS:\n\n\n'
    content += '     # Linux/macOS\n'
    content += '     python3.8 -m pip install -U discord.py\n\n'
    content += '     # Windows\n'
    content += '     py -3.8 -m pip install -U discord.py\n\n'
    content += '4) vscode - vscode is an IDE, aka a code editor and is in my opinion the best one out there. This\n'
    content += '   Is an application and you will use it to write python code for the bot!\n'
    content += '   https://code.visualstudio.com/download\n\n'
    content += '5) SQLiteStudio - another IDE but not for code, for the database! This bot uses a lightweight\n'
    content += '   Relational database - a fancy term that basically says: a database written in the SQL language, but\n'
    content += '   A less heavy duty version of SQL (hence "lite") than regular ol SQL. This IDE makes querying the\n'
    content += '   Database, inserting, and creating new tables much easier.\n\n\n'
    content += 'Now that you have everything you need its time to clone the repository. The repository is on GitHub:\n\n'
    content += '  https://github.com/jesserb/mop-bot\n\n'
    content += 'There you will find all the code for the project, and a green button that says CODE. Clicking the button\n'
    content += 'Offers up a link to "clone" the repository (aka copy the code to your machine). That link is below\n'
    content += 'For convenience:\n\n'
    content += '  https://github.com/jesserb/mop-bot.git\n\n'
    content += 'To clone the repository, simply open up your terminal, navigate to a folder you would like the code to\n'
    content += 'Live in, and run the following command:\n\n'
    content += '  Git clone https://github.com/jesserb/mop-bot.git\n\n'
    content += 'Now when you look at that folder in a file browser you will see all the code! Now git takes some getting\n'
    content += 'Use to, and its important to understand how to use. Here is a link to a complete guide on git, the different\n'
    content += 'Commands, and what it all means for you and your development:\n\n'
    content += '  https://rogerdudler.github.io/git-guide/\n\n\n'
    content += 'NOTE: ONCE YOU HAVE CLONED THE REPOSITORY, you must add the 2 files included in this welcome package to\n'
    content += 'The utils folder. These files are NOT in the git repository as they contain sensitive user information,\n'
    content += 'So we manually have to add those files.\n\n\n'
    content += 'Once you have everything installed, the project cloned, and the included files added in, you can now run\n'
    content += 'The program! Just open up your terminal, navigate to the project folder, and use the following command!\n\n'
    content += '  Python3.8 startup.py MopBotSim1\n\n'
    content += 'For the first time, the terminal will prompt you to enter your username and pin (top of this file). After\n'
    content += 'Authenticating this first time, a session will be created for you ad you will be auto-authenticated every time\n'
    content += 'Here on after!\n\n\n'
    content += 'GOODLUCK!\n'
    content += 'Bop\n\n\n\n\n'
    content += 'SECTION IV\nCODING GUIDE & STRUCTURE\n------------------------------------------------\n\n'
    content += 'Below I briefly describe the coding structure and standards. In the root directory you will\n'
    content += 'Find two folders - /utils and /cogs.\n\n'
    content += '1) /cogs:\n\n'
    content += '   Cogs are for discord bot commands only! You should never define a function hat is not a command,\n'
    content += '   Nor should you be directly querying the database. The idea is to keep these files as clean\n'
    content += '   And short as possible (no small feet with python sadly..) so another developer can easily\n'
    content += '   Get a few for the various commands in each cog. When you go to create a new command, you should\n'
    content += '   first check if your command makes sense to be put in one of the already existing cogs before creating\n'
    content += '   A new one.\n\n'
    content += '2) /utils:\n'
    content += '   If its not a command it probably goes here. There are a few files here:\n\n'
    content += '   - moptest.db - the testing db you will use for development.\n\n'
    content += '   - db.py - a python file for creating functions to interact directly with the DB. All\n'
    content += '     Gets, inserts, updates, removes, etc.. - anything where you need to directly\n'
    content += '     Interact with the DB should go here.\n\n'
    content += '   - functions.py - A python file for all functions that are not commands and do not directly\n'
    content += '     Interact with the DB. For example, you need to get the nickname of a member\n'
    content += '     But all you have is there username. Well from your cog, call a function\n'
    content += '     In function.py that takes in the username, which calls a function\n'
    content += '     From the db.py to get all members in the db, and loop through the results\n'
    content += '     Until you find a match on the username, then return the nickname to you cog!\n\n'
    content += '     Also, try to keep this file organized. There will be a lot of functions\n'
    content += '     In here so keep the Get functions close to each other, the Is functions\n'
    content += '     Close to each other, etc. \n\n'
    content += '     Lastly, before adding a new function check to see if one exists already that\n'
    content += '     Does what you need. If you need to get a member for your command, its likely\n'
    content += '     Another command needed that to and a GetMember function was already created!\n\n'
    content += "   - constants.py - easy file to understand - keep constants there. Aka any variable that's never \n"
    content += '     Going to change!\n\n\n'
    content += 'GIT - so it is expected then whenever your going to work on new development, you should branch\n'
    content += '      Off master. Never push new code directly to master! Complete your task on a separate bench,\n'
    content += '      And if you can try and get another developer to test your code when your finished before\n'
    content += '      Merging the new stuff to master.\n'
    return content






