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

# Get league object to work with
def get_league_info():
	league_id = os.getenv("LEAGUE_ID")
	season = os.getenv("SEASON")
	league = League(league_id, season)

	return league

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

	for user_id in user_list:
		# List of messages - chosen at random
		possible_messages = os.getenv("MESSAGES").split('|')
		chosen_message = randint(0,len(possible_messages) - 1)

		# message users
		sc.api_call(
		  "chat.postMessage",
		  channel=user_id,
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

def send_messages():
	# map slack user ID to team ID
	user_team_map = {
	"U25PVRSP3":2, #will
	# "U25QNG8HJ":6, #doug
	# "U25QQ2FNJ":8, #anne
	# "U25R9407P":7, #kevin
	# "U2643RZBN":1, #jess
	# "U270ZN6RG":3, #najee SUB FOR PAUL WHEN HE'S IN SLACK
	# "U27EHF5HQ":12, #bill
	# "U27GY87U5":5, #dan
	# "U285M8BRT":14, #khalif
	# "U28626KMY":10, #gina
	}

	league_obj = get_league_info()

	league_teams_info = json.loads(requests.get('http://games.espn.com/ffl/api/v2/teams?leagueId=709724&seasonId=2018').text)

	for user_id, team_id in user_team_map.iteritems():
		# List of messages - chosen at random
		possible_messages = os.getenv("MESSAGES").split('|')
		chosen_message = randint(0,len(possible_messages) - 1)

		for team in league_teams_info["teams"]:
			if team["teamId"] == team_id:
				# message users
				sc.api_call(
				  "chat.postMessage",
				  channel=user_id,
				  as_user="true",
				  attachments=[{
				  	"fallback":possible_messages[chosen_message],
				  	"author_name":team["owners"][0]["firstName"] + " " + team["owners"][0]["lastName"],
				  	"title":team["teamLocation"] + " " + team["teamNickname"],
				  	"title_link":"http://games.espn.com/ffl/clubhouse?leagueId=" + str(os.getenv("LEAGUE_ID")) + "&teamId=" + str(team["teamId"]) + "&seasonId=" + str(os.getenv("SEASON")),
				  	"text":possible_messages[chosen_message],
				  	"thumb_url":team["logoUrl"],
				  	"color":"good",
				  	"footer":"_Go Birds_ -:king-yam:",
				  	# "footer_icon":"https://emoji.slack-edge.com/T25PVRSNM/eagles/b9c49504860c346b.jpg",
				  	"fields":[
				  	{
				  		"title": "Record",
				  		"value":str(team["record"]["overallWins"]) + "-" + str(team["record"]["overallLosses"]),
				  		"short":True
				  	},
				  	{
				  		"title":"Waiver Rank",
				  		"value":team["waiverRank"],
				  		"short":True
				  	},
				  	
				  	],
				  	"actions":[{
				  		"type":"button",
				  		"text":"Check Lineup Now",
				  		"url":"http://games.espn.com/ffl/clubhouse?leagueId=" + str(os.getenv("LEAGUE_ID")) + "&teamId=" + str(team["teamId"]) + "&seasonId=" + str(os.getenv("SEASON"))
				  	}]
				  }]
			  	)

		# for team in league_obj.teams:
			# if team.team_id == team_id:
			# 	print team.team_name
			# 	print team
			# 	# message users
			# 	sc.api_call(
			# 	  "chat.postMessage",
			# 	  channel=user_id,
			# 	  as_user="true",
			# 	  attachments=[{
			# 	  	"fallback":possible_messages[chosen_message],
			# 	  	"title":team.team_name,
			# 	  	"title_link":"http://games.espn.com/ffl/clubhouse?leagueId=" + str(os.getenv("LEAGUE_ID")) + "&teamId=" + str(team.team_id) + "&seasonId=" + str(os.getenv("SEASON")),
			# 	  	"text":possible_messages[chosen_message]
			# 	  }]
			# 	)

# espnapi = json.loads(requests.get('http://games.espn.com/ffl/api/v2/teams?leagueId=709724&seasonId=2018').text)
# print espnapi["teams"][0]["divisionStanding"]

# Get slack bot token from env file 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
slack_token = os.getenv("SLACK_BOT_TOKEN") 
season_active = os.getenv("SEASON_ACTIVE") 

sc = SlackClient(slack_token)

# Check that season is active
if (convert_season_active(season_active)):
	# Send message to users
	# user_list = get_user_list()
	# message_reminder(user_list)
	send_messages()
	print "Reminders sent"
else:
	print "Reminders not sent - season not active"




