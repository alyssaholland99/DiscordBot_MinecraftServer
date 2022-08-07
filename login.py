def run():

    from lib import librarySetup
    librarySetup.checkLibraries() #Check and install libraries

    from lib import setup
    #from lib import online
    import os

    if not os.path.isfile('.env'): #Initial setup
        setup.environment()
    
    os.system("python3 lib/player_login.py") #Run main program
run()