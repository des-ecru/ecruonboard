import os
import re
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI, RateLimitError
from rapidfuzz import fuzz


# Load API keys from environment variables
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]  # Starts with xapp-
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

app = App(token=SLACK_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# Load FAQ data
with open("faq.json", "r") as f:
    FAQ = json.load(f)


def get_faq_answer(user_text: str):
    """Return the best FAQ answer if similarity > 70%, else None"""
    text = user_text.lower()
    best_match = None
    highest_score = 0

    for question, answer in FAQ.items():
        score = fuzz.partial_ratio(question.lower(), text)  # 0–100
        if score > highest_score:
            highest_score = score
            best_match = answer

    return best_match if highest_score > 70 else None


@app.message(re.compile(".*"))
def handle_message(message, say):
    """Handles direct messages only"""
    # Only respond in DMs
    if message.get("channel_type") != "im":
        return

    user_text = message.get("text", "")

    # Step 1: Try FAQ
    faq_answer = get_faq_answer(user_text)
    if faq_answer:
        say(faq_answer)
        return

    # Step 2: Fallback to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI coworker helping new employees onboard. "
                        "Only answer from company FAQ and onboarding context."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
        )
        answer = response.choices[0].message.content
        say(answer)

    except RateLimitError:
        say("⚠️ Sorry, I can't process requests right now — OpenAI quota has been exceeded. Please check billing.")


@app.event("app_mention")
def handle_app_mention(event, say):
    """Handles @mentions in channels"""
    user_text = event.get("text", "")

    # Step 1: Try FAQ
    faq_answer = get_faq_answer(user_text)
    if faq_answer:
        say(faq_answer)
        return

    # Step 2: Fallback to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI coworker helping new employees onboard."},
                {"role": "user", "content": user_text},
            ],
        )
        say(response.choices[0].message.content)

    except RateLimitError:
        say("⚠️ Sorry, I can't process requests right now — OpenAI quota has been exceeded. Please check billing.")


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
