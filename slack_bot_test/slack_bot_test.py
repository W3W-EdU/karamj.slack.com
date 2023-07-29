import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

try:
    response = client.chat_postMessage(
        channel="C05KJQ48JDP",
        text="Hello from your app! :tada:"
    )
except SlackApiError as e:
    assert e.response["error"]   

