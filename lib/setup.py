def environment():
    import os
    
    '''Prevents overwriting of the environment file'''
    settingList = ["Token", "Server address/IP", "Port", "Command Prefix", "Custom File", "Server Map", "World Downloads", "Anti Spam", "Owner Name"]
    if os.path.isfile('.env'): #Checks to see if there is an environment file
        overwrite = input("Would you like to change your current settings? (y/n) > ")
        overwrite = overwrite.lower() #Makes the input string lowercase
        if overwrite == "y" or overwrite == "yes":
            print("\nChoose settings to change")
            for i in settingList:
                print("{} - {}".format((settingList.index(i)+1), i)) #Lists all the options to set
            settingsChoice = input("\nInput the numbers of the settings you want to change\nYou can change multiple numbers by typing more than one (Example: 12345)\n > ")
        else:
            return #Exit function
    else: #If the environment file has not been set
        settingsChoice = ""
        for s in range(1, len(settingList)+1): #Goes through all the options and selects all of them to set
            settingsChoice = settingsChoice + str(s)

    '''Gets information'''
    if str(settingList.index("Token")+1) in settingsChoice:
        token = input("Input your bot token here > ")
    else:
        token = os.environ['TOKEN']

    '''Sets the IP/address of the server'''
    if str(settingList.index("Server address/IP")+1) in settingsChoice:
        serverIP = input("Input your server address/IP here > ")
        differentIP = input("Is this different from the public URL/IP? (y/n) > ")
        differentIP = differentIP.lower()
        if differentIP == "y" or differentIP == "yes":
            externalIP = input("Input the public server address here > ")
        else:
            externalIP = serverIP
    else:
        serverIP = os.environ['SERVER']
        externalIP = os.environ['EXTSERVER']

    '''Sets the port used for the minecraft server'''
    if str(settingList.index("Port")+1) in settingsChoice:
        port = input("Input your server port here (If you don't know it, leave blank) > ")
        if port == "":
            port = "25565" #Default Minecraft server port
    else:
        port = os.environ['PORT']

    '''Sets the prefix for the command usage'''
    if str(settingList.index("Command Prefix")+1) in settingsChoice:
        commandPrefix = input("If you want a custom command prefix, enter is here (Default is '?' - Leave bank for default)> ")
        if commandPrefix == "":
            commandPrefix = "?"
    else:
        commandPrefix = os.environ['PREFIX']

    '''Sets the option for the custom file'''
    if str(settingList.index("Custom File")+1) in settingsChoice:
        customFile = input("Would you like a custom file to add your code to? (y/n) > ")
        customFile = customFile.lower()
        if customFile == "y" or customFile == "yes":
            if os.path.isfile("Custom.py"):
                newCustom = input("Do you want to overwrite the current custom file? (y/n) > ")
                newCustom = newCustom.lower()
                if newCustom == "y" or newCustom == "yes":
                    oldFile = open("Custom.py", "r")
                    oldCode = oldFile.read()
                    oldFile.close()
                    if not os.path.exists("oldCustom"):
                        os.makedirs("oldCustom")
                    x = 0
                    copied = False
                    while copied == False:
                        backupPath = "oldCustom/custom{}.py".format(x)
                        if not os.path.isfile(backupPath):
                            backupFile = open(backupPath, "w")
                            backupFile.write(oldCode)
                            copied = True
                        x = x + 1
                    template = open("templates/customTemplate.py", "r")
                    customFile = open("Custom.py", "w")
                    customFile.write(template.read())
                    customFile.close()
                    template.close()
            else:
                template = open("templates/customTemplate.py", "r")
                customFile = open("Custom.py", "w")
                customFile.write(template.read())
                customFile.close()
                template.close()
            custom = "TRUE"
    else:
        custom = "FALSE"
        custom = os.environ['CUSTOM']

    '''Sets the URL for the server map'''
    if str(settingList.index("Server Map")+1) in settingsChoice:
        mapCheck = input("Do you have an online map on your server? (y/n) > ")
        mapCheck = mapCheck.lower()
        if mapCheck == "y" or mapCheck == "yes":
            mapURL = input("What's the URL of the map? (Leave blank if you can't remember, you can set it later) > ")
            if mapURL == "":
                mapURL = "There is no URL set for the map"
        else:
            mapURL = input("There is no online map on this server")
    else:
        mapURL = os.environ['MAP']
    
    '''Set the world download URL'''
    if str(settingList.index("World Downloads")+1) in settingsChoice:
        worldCheck = input("Do you have an online world download on your server? (y/n) > ")
        worldCheck = worldCheck.lower()
        if worldCheck == "y" or mapCheck == "yes":
            worldURL = input("What's the URL of the download? (Leave blank if you can't remember, you can set it later) > ")
            if worldURL == "":
                worldURL = "There is no URL set for the download"
        else:
            worldURL = input("There is no online map on this server")
    else:
        worldURL = os.environ['DOWNLOAD']
    
    '''Sets the anti-spam variable'''
    if str(settingList.index("Anti Spam")+1) in settingsChoice:
        spam = input("Stop users from spamming commands? (y/n) > ")
        spam = spam.lower()
        if spam == "y" or spam == "yes":
            antiSpam = "TRUE"
        else:
            antiSpam = "FALSE"
    else:
        antiSpam = os.environ['ANTISPAM']

    '''Sets the name of the server owner'''
    if str(settingList.index("Owner Name")+1) in settingsChoice:
        owner = input("What's the name of the server owner? > ")
    else:
        owner = os.environ['ADMINNAME']

    '''Concantinate into a string'''
    data = "TOKEN={}\nSERVER={}\nEXTSERVER={}\nPORT={}\nPREFIX={}\nCUSTOM={}\nMAP={}\nDOWNLOAD={}\nANTISPAM={}\nADMINNAME={}".format(token,serverIP,externalIP,port,commandPrefix,custom,mapURL,worldURL,antiSpam,owner) #Sets the format of the data

    '''Write data to the .env file'''
    creds = open(".env", "w")
    creds.write(data)
    creds.close()

    '''Verify the data has been written'''
    print("\nVerifying data..")
    verify = open(".env")
    readData = verify.read()
    verify.close()
    if data == readData:
        print("Data written successfully")
        return
    else:
        tryAgain = ("Error writing data. \n Try again? (y/n) > ")
        tryAgain = tryAgain.lower() #Makes the input string lowercase
        if tryAgain == "y" or tryAgain == "yes":
            environment()
        else:
            return
