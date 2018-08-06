import os
from os.path import join, dirname
from random import randint
from slackclient import SlackClient # need slackclient (install via pip)
import json
from dotenv import load_dotenv # need python-dotenv (install via pip)
import requests
from espnff import League # need espnff (install via pip)


# TODO use ESPN FFL API (maybe NFL api?) to grab meaningful info to send along with the reminder 
# see here:	https://stmorse.github.io/journal/espn-fantasy-python.html
# (players on BYE? teams on BYE? teams playing that day? current score vs opponent?)
# match slack user IDs to team IDs to grab individual data



# Get all users that are in the fantasy football channel for the message_reminder function
def get_user_list():
	final_users_list = []

	# Get all users:
	full_users_list = json.loads(json.dumps(sc.api_call("users.list")))["members"]

	# Only want to message users in #fantasyfootball
	channels_list_return = json.loads(json.dumps(sc.api_call("channels.list",exclude_archived="true")))["channels"]
	members_in_ff_channel = []

	for channel in channels_list_return: 
		# if (channel["id"] == "C4NJ13XUY"): #####TESTING####
		if (channel["id"] == "CC46T3ER5"):
			for member_id in channel["members"]:
				members_in_ff_channel.append(member_id)

	for user in full_users_list:
		if (not user["is_bot"] and not user["deleted"] and not user["id"] == "USLACKBOT" and user["id"] in members_in_ff_channel):
			final_users_list.append(user["id"])

	return final_users_list

# Send message to users in the user list
def message_reminder(user_list):

	for user in user_list:
		# List of messages - chosen at random
		possible_messages = os.getenv("MESSAGES").split('|')

		chosen_message = randint(0,len(possible_messages) - 1)

		# message users
		sc.api_call(
		  "chat.postMessage",
		  channel=user,
		  text=possible_messages[chosen_message],
		  as_user="true"
		)

# Convert var to a boolean value
def convert_season_active(env_var):
	if env_var in ["True", "true", "1"]:
		return True
	elif env_var in ["False", "false", "0"]:
		return False
	else:
		return False


# Get slack bot token from env file 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Token from ENV (
slack_token = os.getenv("SLACK_BOT_TOKEN") 
season_active = os.getenv("SEASON_ACTIVE") 



sc = SlackClient(slack_token)

if (convert_season_active(season_active)):
	user_list = get_user_list()
	message_reminder(user_list)
	print "Reminders sent"
else:
	print "Reminders not sent - season not active"




