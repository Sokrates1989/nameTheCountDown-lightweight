## Start this script, to make the NameTheCountdownBot listen to messages.
## Mentionable functions: 
##      handle_callback_query() handles callbacks of keyboardbuttons that 
##              require different responses to user messages.
##      actUponAnyNonCommandTextMessage() handles user messages that are no commands.
##              This is especially relevant if the directly previously executed 
##              command requires further input.
## At the end of the script the actual polling for user commands is executed.

# Api for listening to bot commands.
import telebot
import time

# Alternative bot.
import telepot

# To get config json.
import json

# To sanitize string (advanced string operations).
import re

# Import own classes.
# Insert path to utils to allow importing them.
import os
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "utils"))
import databaseWrapper as DatabaseWrapper

## Initialize vars.

# Get config.
config_file_pathAndName = os.path.join(os.path.dirname(__file__), "config.txt")
config_file = open(config_file_pathAndName)
config_array = json.load(config_file)

# Instantiate classes.
# Database connection.
dbWrapper = DatabaseWrapper.DatabaseWrapper()

# Initialize bots.
botToken = config_array["telegram"]["botToken"]
bot = telebot.TeleBot(botToken, parse_mode="HTML")
telepotBot = telepot.Bot(botToken)


# Always save the last used command to var to allow follow up interaction.
# To interact with this var you need to use getter and setter functions below.
lastUsedCommand = {}

# If messages have to be split into multiple messages -> let user load next message by button click.
individualMessagesToSend = {}
lastSentMessage = {}

def getLastUsedCommand(userID):
    key = str(userID)
    if key in lastUsedCommand:
        return lastUsedCommand[key]
    else:
        return "None"

def setLastUsedCommand(command, userID):
    global lastUsedCommand
    key = str(userID)
    lastUsedCommand[key] = str(command)


## Declare functions.

# Get parameter of text message.
def extractParametersFromMessageText(originalMessage):
    originalMessage = sanitizeString(originalMessage)
    # Does message start with command?
    if originalMessage.startswith("/"):
        return originalMessage.split()[1:]
    else:
        return originalMessage.split()

# Get username from message.from_user.first_name.
def getUserName(messageFrom_userFirst_name):
    userName = ""
    if (messageFrom_userFirst_name != None):
        userName = sanitizeString(messageFrom_userFirst_name)
    return userName

# Get user from message.chat.id or create a new user, if there is none.
def getUserFromMessage(message):

    # Must always renew database connection, when interacting with DB, because it caches its values.
    global dbWrapper
    dbWrapper = DatabaseWrapper.DatabaseWrapper()

    user = dbWrapper.getUserByChatID(int(message.chat.id))
    if user == None:
        # Create user, if not existing yet.
        user = dbWrapper.createNewUser(getUserName(message.from_user.first_name), int(message.chat.id))

    return user

# Removes unwanted characters from a string (only allows whitelisted characters).
def sanitizeString(stringToSanitize):
    whiteListedCharactersRegEx = "[^a-zA-Z0-9:=/._?&!äöü+ ]"
    return re.sub(whiteListedCharactersRegEx, '', str(stringToSanitize) )
    
## Listen to user commands.

# Listen to bot commands start and help.
@bot.message_handler(commands=['countdown', 'start'])
def countdown(message):

    # Set last used command user based, to allow interaction with none command text messages.
    user = getUserFromMessage(message)
    setLastUsedCommand("countdown", user["ID"])

    # Tell user to name the countdown.
    userMsg = "Please tell me the name for your new countdown"
    bot.send_message(user["chatID"], userMsg )




## Listen to any text that is not a previously declared command.
@bot.message_handler(func=lambda message: True)
def actUponAnyNonCommandTextMessage(message):

    # Get last executed command.
    user = getUserFromMessage(message)
    lastUsedCommandOfUser = getLastUsedCommand(user["ID"])

    # Always reset last used command, if follow up interaction is successful, to avoid redundant calls.
    # Set last used command user based, to allow interaction with none command text messages.
    setLastUsedCommand("None", user["ID"])

    # Is last used command set?
    if (lastUsedCommandOfUser != "None"):

        parameters = lastUsedCommandOfUser.split("-")
        if lastUsedCommandOfUser.startswith("countdown"):
            extracted = extractParametersFromMessageText(message.text)
            nameCountdown_callback(message, extracted, user["ID"])
        elif lastUsedCommandOfUser.startswith("duration-"):
            countdownName = parameters[1]
            extracted = extractParametersFromMessageText(message.text)
            setDuration_callback(message, countdownName, extracted, user["ID"])
        else:
            # Execute last used command with user input again.
            globals()[lastUsedCommandOfUser](message)
    else:
        bot.reply_to(message, "sry, I do not know what to do now.. \n\nIf a command has been successfully executed, you must use a command again. This prevents unwanted interactions.\n\nPress here: /countdown")


# Follow up after asking for naming countdown. Asks for duration (in minutes).
def nameCountdown_callback(message, extractedParameterFromMessage, userID):

    # Set last used command, so user can simply paste other countdown name, in case of an error.
    setLastUsedCommand("countdown", userID)

    # Get user by his id.
    user = dbWrapper.getUserByID(userID)

    # Is extracted parameter valid?
    if (len(extractedParameterFromMessage) != 0):

        # Get the name, the user gave to countdown.
        countdownName = extractedParameterFromMessage[0]

        # Set last used command, so user can now set duration for that timer.
        setLastUsedCommand("duration-" + str(countdownName), userID)

        # Tell user to now send duration in minutes.
        userMsg = "How long should the countdown take?\nPlease enter the amount of minutes."
        bot.send_message(user["chatID"], userMsg )

            
    else:
        userMsg = "Please tell me the name for your new countdown"
        bot.send_message(user["chatID"], userMsg )


# Set duration of countdown.
def setDuration_callback(message, countdownName, extractedParameterFromMessage, userID):

    # Get user by his id.
    # Update DB.
    dbWrapper = DatabaseWrapper.DatabaseWrapper()
    user = dbWrapper.getUserByID(userID)

    # Set last used command, so user can simply paste other duration, in case of an error.
    setLastUsedCommand("duration-" + str(countdownName), userID)

    # Is extracted parameter valid?
    if (len(extractedParameterFromMessage) != 0):

        # Is Parameter a number?
        duration = extractedParameterFromMessage[0]
        if duration.isnumeric():

            # The duration is correct -> reset last usedCommand.
            setLastUsedCommand("None", userID)

            dbWrapper.createNewCountdownForUser(userID, countdownName, duration)

            userMsg = "I send you a message once your countdown \"" + str(countdownName) + "\" finishes in " + str(duration) + " minute(s)."
            bot.send_message(user["chatID"], userMsg )
            

        else:
            userMsg = "Please enter the duration of the countdown in minutes. (numbers only)"
            bot.send_message(user["chatID"], userMsg )
            
    else:
        userMsg = "Please enter the duration of the countdown in minutes."
        bot.send_message(user["chatID"], userMsg )
     




## Start polling for commands.
print("Listening ...")
bot.polling(none_stop=False, interval=1)

while True:
    try:

        # Listen to text messages sent to the Bot.
        print("Listening ...")
        bot.polling(none_stop=False, interval=1)
        

    except Exception as e:
        print("An Error occured while polling commands" + e)

        # Sleep 1 second.
        time.sleep(1)