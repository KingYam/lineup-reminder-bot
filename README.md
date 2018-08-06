# lineup-reminder-bot
A reminder Slackbot for my fantasy football league Slack team.

This runs only at certain times (based on NFL schedule; using crontab on my server) and sends direct message reminders to members of our #fantasyfootball slack channel.

### Dependencies
* slackclient
* python-dotenv

Not featured in repo: .env file which includes the slack token for custom bot and other environmental variables.