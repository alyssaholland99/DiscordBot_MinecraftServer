def customCode(inputMessage, message):
    import os
    prefix = os.environ['PREFIX'] #This gets the prefix 
    if not inputMessage[:len(prefix)]: #Checks to see if the prefix is at the start of the message
        return message  #If it isn't, ignore the rest of the code
    inputMessage = inputMessage[len(prefix):]
    '''Do not modify any code above this'''
    

    if inputMessage == "example":
        message = "This is an example of the custom code you can write"
    elif inputMessage == "example2":
        message = "This is also an example of the custom code you can write"
        
        
        
    '''Do not modify any code below this'''    
    return message #Send the message back to the main program