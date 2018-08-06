# lineup-reminder-bot
A reminder Slackbot for my fantasy football league Slack team.

This runs only at certain times (based on NFL schedule; using crontab on my server) and sends direct message reminders to members of our #fantasyfootball slack channel.

### Dependencies
* [slackclient](https://github.com/slackapi/python-slackclient)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [espnff](https://github.com/rbarton65/espnff)

Not featured in repo: .env file which includes the slack token for custom bot and other environmental variables.

### Future TO-DOs
* Add [ESPN FFL API](https://stmorse.github.io/journal/espn-fantasy-python.html) calls (try using espnff) to grab indivdual team/matchup info to make notifications more useful
