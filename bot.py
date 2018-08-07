import os
from os.path import join, dirname
from random import randint
from slackclient import SlackClient
import json
from dotenv import load_dotenv
import requests

# Convert var to a boolean value
def convert_season_active(env_var):
	if env_var in ["True", "true", "1"]:
		return True
	elif env_var in ["False", "false", "0"]:
		return False
	else:
		return False

def get_ineligible_players(team_ID):

	bye_count = 0
	injured_count = 0

	scoreboard_info = json.loads(requests.get("http://games.espn.com/ffl/api/v2/scoreboard?leagueId=" + str(os.getenv("LEAGUE_ID")) + "&seasonId=" + str(os.getenv("SEASON")) + "&teamId=" + str(team_ID)).text)
	teams = scoreboard_info["scoreboard"]["matchups"][0]["teams"]

	# Set current team
	current_team = {}
	for team in teams:
		if team["teamId"] == team_ID:
			current_team = team


	# Players on roster
	# String for use in API call

	if len(current_team["playerIDs"]) > 0:
		current_team_players_string = ",".join(map(str,current_team["playerIDs"]))
		api_players_info = json.loads(requests.get("http://games.espn.com/ffl/api/v2/playerInfo?leagueId=" + str(os.getenv("LEAGUE_ID")) + "&seasonId=" + str(os.getenv("SEASON")) + "&playerId=" + current_team_players_string).text)
		
		# Used for finding BYEs
		progames = api_players_info["playerInfo"]["progames"]
		pro_teams_playing = []
		for progame in progames:
			pro_teams_playing.append(progames[progame]["awayProTeamId"])
			pro_teams_playing.append(progames[progame]["homeProTeamId"])

		players = api_players_info["playerInfo"]["players"]
		for player in players:
			if player["player"]["healthStatus"] > 1:
				injured_count += 1
			if player["player"]["proTeamId"] not in pro_teams_playing:
				bye_count += 1

		return {"byeCount": bye_count, "injuredCount": injured_count}
	else:
		return {"byeCount": -1, "injuredCount": -1}

def send_messages():
	# map slack user ID to team ID
	with open(os.getenv("USER_MAP_FILE_NAME")) as t:
		user_team_map = json.load(t)

	league_teams_info = json.loads(requests.get("http://games.espn.com/ffl/api/v2/teams?leagueId=" + str(os.getenv("LEAGUE_ID")) + "&seasonId=" + str(os.getenv("SEASON"))).text)

	for user_id, team_id in user_team_map.iteritems():
		# List of messages - chosen at random
		possible_messages = os.getenv("MESSAGES").split('|')
		chosen_message = randint(0,len(possible_messages) - 1)

		ineligible_players = get_ineligible_players(team_id)

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
				  	"footer":"_Go Birds_ -:king-yam:	Contact Will if you see any issues.",
				  	"fields":[
				  	{
				  		"title":"Players on BYE",
				  		"value":ineligible_players["byeCount"],
				  		"short":True
				  	},
				  	{
				  		"title":"Players Injured",
				  		"value":ineligible_players["injuredCount"],
				  		"short":True
				  	},
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
				  		"text":"Review Roster",
				  		"url":"http://games.espn.com/ffl/clubhouse?leagueId=" + str(os.getenv("LEAGUE_ID")) + "&teamId=" + str(team["teamId"]) + "&seasonId=" + str(os.getenv("SEASON"))
				  	}]
				  }]
			  	)



# Get slack bot token from env file 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
slack_token = os.getenv("SLACK_BOT_TOKEN") 
season_active = os.getenv("SEASON_ACTIVE") 

sc = SlackClient(slack_token)

# Check that season is active
if (convert_season_active(season_active)):
	# Send message to users
	send_messages()
	print "Reminders sent"
else:
	print "Reminders not sent - season not active"




