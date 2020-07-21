"""
Slackbot that uses Flask and Slack Events API under the hood
Events URL: https://ee71d7256a30.ngrok.io/slack/events
"""

from flask import Flask, escape, request
import os
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
import json
import logging
from slack import WebClient


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
load_dotenv()
signing_secret = os.environ["SLACK_SIGNING_SECRET"]

slack_events = SlackEventAdapter(signing_secret, "/slack/events", app)

web_client = WebClient(os.environ["SLACK_BOT_TOKEN"])

# @app.before_request
def logrequests():
    app.logger.debug(json.dumps(request.json, indent=4))

@app.route('/')
def hello():
    name = request.args.get("name", "Kenzie")
    return f'Hello, {escape(name)}!'

@slack_events.on("app_mention")
def appmention(payload):
    event = payload.get("event", {})
    channel = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    web_client.chat_postMessage(channel=channel, text=f"Received message from {user_id}: {text}")

@slack_events.on("message")
def message(payload):
    event = payload.get("event", {})
    channel = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    bot_id = event.get("bot_id")
    if bot_id is not None:
        app.logger.info(f"I discarded the message from {bot_id}")
    else:
        web_client.chat_postMessage(channel=channel, text=f"Received message from {user_id}: {text}")
    