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

# Get all users:
full_users_list = json.loads(json.dumps(sc.api_call("users.list")))

# Only want to message users in #fantasyfootball
channels_list_return = json.loads(json.dumps(sc.api_call("channels.list",exclude_archived="true")))["channels"]
members_in_ff_channel = []

for channel in channels_list_return:
	# print channel["name"]
	if (channel["name"] == "fantasyfootball"):
		for member_id in channel["members"]:
			members_in_ff_channel.append(member_id)



print full_users_list["members"][0]["name"]

# List of messages - chosen at random
possible_messages = ["Hey! This is your reminder to check on your lineup before games start today. Best of luck!",
"*YO* - this is your reminder: check your roster! No one wants to see your opponent win because you didn't replace that TE you have on BYE.",
"something NOT useful"]

chosen_message = randint(0,len(possible_messages) - 1)

sc.api_call(
  "chat.postMessage",
  channel="@wfoley",
  text=possible_messages[chosen_message],
  as_user="true"
)
