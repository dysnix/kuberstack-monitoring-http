from slackclient import SlackClient
from settings import SLACK_TOKEN, SLACK_CHANNEL, CLUSTER_NAME

sc = SlackClient(SLACK_TOKEN)

NORMAL_COLOR = '#36a64f'
WARNING_COLOR = '#FFFF00'
ERROR_COLOR = '#FF0000'

ALERTS_COLORS = {
    'Normal': NORMAL_COLOR,
    'Warning': WARNING_COLOR,
}


def get_slack_msg_color(event_type):
    return ALERTS_COLORS.get(event_type, ERROR_COLOR)


def send_alert(event_type, url, description, status, response_time):
    attachment = {
        "fallback": description,
        "color": get_slack_msg_color(event_type),
        "title": description,
        "title_link": url,
        "fields": [
            {
                "title": "URL",
                "value": url
            },
            {
                "title": "Status",
                "value": status
            },
            {
                "title": "Response time",
                "value": response_time
            }
        ],
        "footer": CLUSTER_NAME,
    }

    sc.api_call(
        "chat.postMessage",
        channel=SLACK_CHANNEL,
        attachments=[attachment]
    )
