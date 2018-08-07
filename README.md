# lineup-reminder-bot
A reminder Slackbot for my fantasy football league Slack team.

This runs only at certain times (based on NFL schedule; using crontab on my server) and sends direct message reminders to members of our #fantasyfootball slack channel. 

The reminder includes individual team data such as:
* Number of players on their BYE week
* Number of players with an injury status of Questionable or higher
* Waiver wire rank
* Current team record
* Link to team roster page

### Dependencies
* [slackclient](https://github.com/slackapi/python-slackclient)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

Not featured in repo: .env file which includes the slack token for custom bot and other environmental variables.


