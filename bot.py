import os
from os.path import join, dirname
from random import randint
from slackclient import SlackClient
import json
from dotenv import load_dotenv

# Get slack bot token from env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Token from ENV
slack_token = os.getenv("SLACK_BOT_TOKEN")
sc = SlackClient(slack_token)

# Get all users that are in the fantasy football channel for the message_reminder function
def get_user_list():
	final_users_list = []

	# Get all users:
	full_users_list = json.loads(json.dumps(sc.api_call("users.list")))["members"]

	# Only want to message users in #fantasyfootball
	channels_list_return = json.loads(json.dumps(sc.api_call("channels.list",exclude_archived="true")))["channels"]
	members_in_ff_channel = []

	for channel in channels_list_return:
		if (channel["id"] == "C4NJ13XUY"):
			for member_id in channel["members"]:
				members_in_ff_channel.append(member_id)

	for user in full_users_list:
		if (not user["is_bot"] and not user["deleted"] and not user["id"] == "USLACKBOT" and user["id"] in members_in_ff_channel):
			final_users_list.append(user["id"])

	return final_users_list

# Send message to users in the user list
def message_reminder(user_list):

	# List of messages - chosen at random
	possible_messages = ["Hey! This is your reminder to check on your lineup before games start today. Best of luck!",
	"*YO* - this is your reminder: check your roster! No one wants to see your opponent win because you didn't replace that TE you have on BYE.",
	"something NOT useful"]

	chosen_message = randint(0,len(possible_messages) - 1)

	# message users
	sc.api_call(
	  "chat.postMessage",
	  channel="@wfoley",
	  text=possible_messages[chosen_message],
	  as_user="true"
	)
user_list = get_user_list()
# message_reminder(user_list)




