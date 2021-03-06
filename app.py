import stackexchange
import builtins
import os
import requests
from flask import Flask, request, make_response
from json import loads
from slackclient import SlackClient
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

STACKEXCHANGE_APP_TOKEN = os.getenv("STACKEXCHANGE_APP_TOKEN")
so = stackexchange.Site(stackexchange.StackOverflow, STACKEXCHANGE_APP_TOKEN)
so.impose_throttling = True
so.throttle_stop = False
so.be_inclusive()

message = """*<{url}|{title}>* by {owner.display_name}
{creation_date}
{body}
"""

message_sans_owner = """*<{url}|{title}>*
{creation_date}
{body}
"""

def query_so(tags=[], order="desc", sort="creation"):

    return so.questions.no_answers(order=order, sort=sort, tagged=tags).fetch()

def create_question_text(unanswered_questions):

    total_output = """
    *SO Questions w/o responses:*

"""

    for question in unanswered_questions[:10]:

        question.body = question.body[:250] + "..." if len(question.body) > 250 else question.body

        question.body = question.body.strip()

        question.body = strip_tags(question.body)

        if "owner" in question.__dict__:
            total_output += message.format(**question.__dict__)
        else:
            total_output += message_sans_owner.format(**question.__dict__)

        total_output += "\n\n"

    return total_output


app = Flask(__name__)

@app.route("/status", methods=["GET"])
def app_status():


    slack_ready = True if "SLACK_TOKEN" in os.environ else False
    stackoverflow_ready = True if "STACKEXCHANGE_APP_TOKEN" in os.environ else False

    response_text = u"""
    <div style="margin-top:10%;margin-left:auto; margin-right:auto; width:20%">
    <h1>SO Unanswered Bot</h1>
    <p>Slack API Token Set => <strong>{}</strong></p>
    <p>StackExchange App Token Set => <strong>{}</strong></p>
    """.format(slack_ready, stackoverflow_ready)

    response = make_response(response_text)

    return response

@app.route("/", methods=["POST"])
def unanswered_questions():
    if request.values["token"] == os.environ["SLACK_SLASH_TOKEN"]:
        tags = request.values["text"].split(",")

        unanswered_questions = query_so(tags = tags)
        response_text = create_question_text(unanswered_questions)

        payload = dict(
            channel = "#{}".format(request.values.get("channel_name")),
            text = response_text,
        )

        r = requests.post(
            os.environ["SLACK_WEBHOOK_URL"],
            json=payload,
            headers= {"Content-Type": "application/json"}
        )

        return ("", 200)
    else:
        return ("", 403)

if __name__ == "__main__":
    app.run("0.0.0.0")
