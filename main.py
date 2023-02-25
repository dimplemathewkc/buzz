import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App


# Event API and web api
slack_app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def handle_message(body, logger):
    print(str(body["event"]["text"]).split(">")[1])
    prompt = str(body["event"]["text"]).split(">")[1]

    response = slack_client.chat_postMessage(
        channel=body["event"]["channel"],
        thread_ts=body["event"]["ts"],
        text="Thinking... :bee:",
    )

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    response = (
        openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        .choices[0]
        .text
    )

    # reply to the message
    response = slack_client.chat_postMessage(
        channel=body["event"]["channel"],
        thread_ts=body["event"]["ts"],
        text=f"Here you go: \n{response}",
    )

    if __name__ == "__main__":
        SocketModeHandler(slack_app, os.environ.get('SLACK_APP_TOKEN')).start()
