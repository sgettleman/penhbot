#Import everyting that is needed
import os
import logging
import re
from datetime import date
from dotenv import load_dotenv
from flask import Flask
import slack_sdk
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slackeventsapi import SlackEventAdapter
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

#App and Bot Tokens
app = App(token=os.environ["SLACK_BOT_TOKEN"])
client=slack_sdk.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

#Load tokens
env_path = ".env"
load_dotenv(env_path)

#Define response message and button

trigger_phrase = ["feature request", "bug report", "report a bug"]

#Listening for the phrase "feature request"
@app.message("")
def message_hello(message, say):
    if any(phrase.casefold() in message['text'].casefold() for phrase in trigger_phrase):
        try:
            say(
            blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"In order to submit a feature request or bug report, please click below to be taken to the PENH Jira board."}, 
            },
            {
                "type": "actions",
                "elements": [
                    { 
                        "type": "button",
                        "style": "primary",
                        "text": {"type": "plain_text", "text": f"PENH Board"},
                        "value": "click_me",
                        "url": "https://veracode.atlassian.net/jira/software/c/projects/PENH/boards/309",
                        "action_id": "button_click"
                    },
                ]
            }
        ]
    )
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")

@app.command("/feature-request")
def handle_feature_request(ack, respond, command):
    ack()

    feature_request = command['text']

    response_text = (
        f"*I've created a Jira ticket on the PenH board"
        f" called \"{feature_request}\". Please open the ticket and fill in the body"
        f"completey so the PM team can consider it"
    )

    respond(text=response_text)

@app.action("button_click")
def action_button_click(body, ack, say):
    ack()
    say(f"Redirecting to PenH Board!")

@app.event("app_mention")
def event_test(say):
    say("Hi there! Are you looking to submit a feature request or bug request? If so, type 'Feature Request' or 'Bug Report")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_SOCKET_TOKEN"]).start()