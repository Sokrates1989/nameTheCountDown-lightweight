## Start this script, to check, if a countdown finished.

# Api for listening to bot commands.
import telebot
import time

# Alternative bot.
import telepot

# To get config json.
import json

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


## Check whether a scheduled countdown has to be sent.
i = 0
print("checking ...")
while True:
    try:

        # Only print every xth time, that we are still checking.
        i = i + 1
        printEvery = 100
        if (i%printEvery == 0):
            print("checking (" + str(i) + ") ...")

        # Update database connection.
        dbWrapper = DatabaseWrapper.DatabaseWrapper()

        # Are there schdueled countdowns, that have to be send.
        unsendPendingCountDowns = dbWrapper.getUnsendPendingCountdowns()
        if unsendPendingCountDowns: 
            # There are unsend pending countdowns.
            for countdown in unsendPendingCountDowns:

                # Output info.
                print ("found unsent countdown:")
                print (countdown)
                print ("sending mesage now..")
                
                # Send the message to the user.
                user = dbWrapper.getUserByID(countdown["userID"])
                countdownFinishedMsg = "Your timer \"" + str(countdown["name"]) + "\" finished!"
                bot.send_message(user["chatID"], countdownFinishedMsg)

                # Output info.
                print ("message sent!")
                print ("indicating, that message has been sent now..")

                # Indicate to DB, that message has been sent.
                dbWrapper.indicateThatCountdownMessageHasBeenSent(countdown["ID"])
        
                # Output info.
                print ("indicated, that message has been sent!")

        # Sleep 1 second.
        time.sleep(1)

    except Exception as e:
        print("An Error occured while polling commands" + e)

        # Sleep 1 second.
        time.sleep(1)