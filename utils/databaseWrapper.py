### Class for any interaction with the DB
### All write and read operations of DB should be done in this file/ class

## Imports
# database connection.
import mysql.connector
# file sytem operations
import os
# For getting config
import json
# To retrieve current timestamp
import time


class DatabaseWrapper:

	# Constructor.
	def __init__(self):

		# Get credentials for database from config file.
		config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "config.txt")
		config_file = open(config_file_pathAndName)
		config_array = json.load(config_file)

		# Database connection
		self.mydb = mysql.connector.connect(
		host=config_array["database"]["host"],
		user=config_array["database"]["user"],
		password=config_array["database"]["password"],
		database=config_array["database"]["database"],
		port=config_array["database"]["port"]
		)
		self.mycursor = self.mydb.cursor(buffered=True) # need to buffer to fix mysql.connector.errors.InternalError: Unread result found (https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone)




	# Get user by his chatID
	# pass chatID as parameter
	# Return is an associative array or None
	def getUserByChatID(self, chatID):

		query = "SELECT ID FROM users WHERE chatID=%s "
		val = (chatID, )
		self.mycursor.execute(query, val)
		myresult = self.mycursor.fetchone()

		# Did query retrieve valid user?
		user = None
		if (myresult != None):
			user = self.getUserByID(myresult[0])
		return user

	# Get user by his ID
	# pass ID as parameter
	# Return is an associative array or None
	def getUserByID(self, userID):
		query = "SELECT ID, name, chatID FROM users WHERE ID=%s "
		val = (userID, )
		self.mycursor.execute(query, val)
		myresult = self.mycursor.fetchone()

		# Did query retrieve valid user?
		user = None
		if (myresult != None):
			user = {
			'ID': myresult[0],
			'name': myresult[1],
			'chatID': myresult[2]
			}
		return user

		

	# Create new user
	# pass chatID and name (empty or None string, if unknown)
	# Return is an associative array of user
	def createNewUser(self, name, chatID):

		if (name == None):
			name = ""

		# Execute insert query to create a new user.
		insertUserSql = "INSERT INTO users (name, chatID) VALUES (%s, %s)"
		val = (name, chatID)
		self.mycursor.execute(insertUserSql, val)
		self.mydb.commit()

		# Return newly created user.
		return self.getUserByChatID(chatID)




	# Get countdown by its ID.
	# Pass ID as parameter.
	# Return is an associative array or None
	def getCountdownByID(self, countdownID):
		query = "SELECT ID, name, whenToSend, durationInMinutes, hasBeenSent, fk_user_id FROM countdowns WHERE ID=%s "
		val = (countdownID, )
		self.mycursor.execute(query, val)
		myresult = self.mycursor.fetchone()

		# Did query retrieve valid user?
		user = None
		if (myresult != None):
			user = {
			'ID': myresult[0],
			'name': myresult[1],
			'whenToSend': myresult[2],
			'durationInMinutes': myresult[3],
			'hasBeenSent': myresult[4],
			'userID': myresult[5]
			}
		return user


	# Create new countdown for a user.
	def createNewCountdownForUser(self, userID, countdownName, durationInMinutes):

		if (countdownName == None):
			countdownName = ""

		# time.time() returns 8237981234.23784827 -> int(time.time()) returns 8237981234
		whenToSend = int(time.time()) + int(durationInMinutes) * 60

		# Execute insert query to create a new countdown.
		sql = "INSERT INTO countdowns (name, whenToSend, durationInMinutes, hasBeenSent, fk_user_id) VALUES (%s, %s, %s, 0, %s)"
		val = (countdownName, whenToSend, durationInMinutes, userID)
		self.mycursor.execute(sql, val)
		self.mydb.commit()

		# Get newlycreated countdown ID
		newCountDownID = self.mycursor.lastrowid

		# Return newly created countdown.
		return self.getCountdownByID(newCountDownID)




	# Get unsend countdowns, that should be send.
	def getUnsendPendingCountdowns(self):

		now = int(time.time())

		query = "SELECT ID FROM countdowns WHERE hasBeenSent=0 AND whenToSend<%s Order By ID ASC"
		val = (now, )
		self.mycursor.execute(query, val)
		myresults = self.mycursor.fetchall()
	
		unsendPendingCountdowns = []
		for countdownResult in myresults:
			unsendPendingCountdowns.append(self.getCountdownByID(countdownResult[0]))
		return unsendPendingCountdowns



	# Indicate, that a countdown message has been sent.
	def indicateThatCountdownMessageHasBeenSent(self, countdownID):

		sql = "UPDATE countdowns SET hasBeenSent = 1 WHERE ID = %s"
		val = (countdownID, )

		# Execute query.
		self.mycursor.execute(sql, val)
		self.mydb.commit()
