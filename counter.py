import datetime
import requests

# Set your Slack API token
import os
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]

# Target date
TARGET_DATE = datetime.datetime(2025, 8, 1)

# Special trip and event dates
SPECIAL_EVENTS = [
    {
        "start": datetime.datetime(2025, 5, 18),
        "end": datetime.datetime(2025, 5, 19),
        "text": "Concert in Atlanta",
        "emoji": ":musical_note:"
    },
    {
        "start": datetime.datetime(2025, 6, 4),
        "end": datetime.datetime(2025, 6, 6),
        "text": "Concert at the Hollywood Bowl",
        "emoji": ":musical_note:"
    },
    {
        "start": datetime.datetime(2025, 6, 7),
        "end": datetime.datetime(2025, 6, 14),
        "text": "Annual Family Trip to Boca Grande",
        "emoji": ":palm_tree:"
    },
    {
        "start": datetime.datetime(2025, 6, 26),
        "end": datetime.datetime(2025, 6, 29),
        "text": "Trip to Alys Beach",
        "emoji": ":beach_with_umbrella:"
    },
    {
        "start": datetime.datetime(2025, 6, 29),
        "end": datetime.datetime(2025, 7, 2),
        "text": "Smoky Mountains",
        "emoji": ":mountain_biking_man:"
    },
    {
        "start": datetime.datetime(2025, 7, 3),
        "end": datetime.datetime(2025, 7, 5),
        "text": "South Carolina",
        "emoji": ":southcarolina:"
    },
    {
        "start": datetime.datetime(2025, 7, 24),
        "end": datetime.datetime(2025, 7, 27),
        "text": "One last sabbatical beach trip",
        "emoji": ":beach_with_umbrella:"
    }
]

def days_until_target():
    now = datetime.datetime.utcnow()
    delta = TARGET_DATE - now
    return max(delta.days, 0)

def generate_status_text_and_emoji(days_left):
    now = datetime.datetime.utcnow()

    # Check for special events first
    for event in SPECIAL_EVENTS:
        if event["start"] <= now <= event["end"]:
            return event["text"], event["emoji"]
    
    # Special countdown cases
    if days_left == 7:
        return "One week to go!", ":sabbaticalleave:"
    elif days_left == 1:
        return "See you tomorrow!", ":sabbaticalleave:"
    else:
        return f"{days_left} days left", ":sabbaticalleave:"

def update_slack_status(status_text, status_emoji):
    payload = {
        "profile": {
            "status_text": status_text,
            "status_emoji": status_emoji,
            "status_expiration": 0
        }
    }

    response = requests.post(
        "https://slack.com/api/users.profile.set",
        headers={
            "Authorization": f"Bearer {SLACK_API_TOKEN}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    if not response.ok or not response.json().get('ok', False):
        print("Failed to update status:", response.text)
    else:
        print(f"Updated Slack status to: {status_text}")

def main():
    days_left = days_until_target()
    status_text, status_emoji = generate_status_text_and_emoji(days_left)
    update_slack_status(status_text, status_emoji)

if __name__ == "__main__":
    main()
