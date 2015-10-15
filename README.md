# so-unanswered-bot

A deployable SlackBot which will return N unresponded (not unanswered) questions from StackOverflow

The purpose of this app is to be able to get a list of unanswered questions on StackOverflow. Working for @RethinkDB, I want to take every opportunity to reach out to people with questions and the StackExchange network continues to be an excellent place to ask questions and get answers. Quickly querying and getting a list of people still looking for help is pricelesss as a developer evangelist.

This bot just requires two API tokens. One from Slack as well as another one from the StackExchange API. You can get them here:

### Slack Slash Commands Token

To enable the slash command in Slack `/stackoverflow` you just need to [create a new slash command integration by going here](https://rethinkdb-team.slack.com/services/new/slash-commands). You'll want to grab the token that is generated to ensure that your app only responds to your organization's requests.

![](http://i.imgur.com/vUk8fkp.png)

### StackExchange Token
https://stackapps.com/users/login?returnurl=/apps/oauth/register

Once you have these two things handy, you're ready to deploy!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/dalanmiller/so-unanswered-bot)
