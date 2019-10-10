This bot uses a [mattermost incoming webhook](https://docs.mattermost.com/developer/webhooks-incoming.html) 
to sent messages derived from gitlab [application.log](https://docs.gitlab.com/ee/administration/logs.html#applicationlog) file.

This could be a notification to the user of successful or failed login events (which is done by default).

# Config
Copy [`.env.dist`](.env.dist) to `.env` and change the variables to your needs.

**Note:** Make sure the user you will run the bot can at least read the file at `HOST_GITLAB_APPLICATION_LOG_FILE`
 
# Start
Run the bot via docker-compose `docker-compose up -d`

# Limitations
## Direct messages to a user.
Mattermost incoming webhooks can only sent messages directly to a chat. This means to sent direct messages to a user,
 the "from user" will be the user who created the bot but in that chat, the message will be originated from the bot.

# Extensions
Take a look into the `EVENTS` dict in [bot.py](bot.py). You can add more events. Use named regex group to use the 
results in the channel and message template.
