import json
import requests
import uuid
from youtubesearchpython import VideosSearch

CONVERSATION_ID = uuid.uuid4()
topics = []
research_opportunities = []
study_resources = []

def call_otherside(message):
    global CONVERSATION_ID
    headers = {"Authorization":"953cb18c44514eb0b94bf0d1422871cfbb47c7c2d98c498595823dc780226572741308caf303480d9b8b59bc2d43da05b5d86acb8f874fb9b6393f2c36f1450f"}

    data = {
        'payload':json.dumps({'message': message, 'chatId': str(CONVERSATION_ID)})
    }
    r = requests.post('http://api.hyperwriteai.com/api/v1/generateViaAPI', headers=headers, data=data)

    return r.json()['message']

def summarize_research_opps():
    res = call_otherside("Please summarize the list of open problems and unanswered academic questions from this conversation that could be novel research opportunities for a new graduate? Put each point on a separate line")
    print(res)
    for line in res.split("\n"):
        research_opportunities.append(line)

def summarize_topics():
    res = call_otherside("Please summarize the list of topics we discussed in this conversation so I can review them later. Put each topic on a separate line")
    print(res)
    for line in res.split("\n"):
        topics.append(line)

def conversation_loop():
    line = input()
    response = call_otherside(line)
    summarize_research_opps()
    summarize_topics()
    print(response)
    print("\n\n")

def fetch_learning_resources(topics):
    topics = ["How to sleep better", "how sleep recovers brain cells"]
    for topic in topics:
        videosSearch = VideosSearch(topic, limit = 1)
        for res in videosSearch.result()['result']:
            print(res.get("title", "") + " | " + res.get("link", ""))
            study_resources.append({"title": res.get("title", ""), "link": res.get("link","")})

def find_mentors():
    for topic in topics:
        res = call_otherside("I want to learn more about the topic of " + topic + ". What query should I write in Linkedin search to find a mentor who specialize and work in this topic?")
        print("Query for topic: " + topic + " is: " + res)

def conversation_loop():
    line = input()

    if line == "summarize":
        summarize_research_opps()
        summarize_topics()
        fetch_learning_resources()
        find_mentors()
        return

    response = call_otherside(line)
    print(response)
    print("\n\n")

# blocker: how to partition conversation into chunks to get context, without overlapping topics
def interview():
    age = input("How old are you?")
    name = input("What's your name?")
    education = input("What is your highest level of education?") 
    specialty = input("What are your occupations/specialties?")

    age = 26
    name = "kyle"
    education = "gradschool"
    specialty = "mathematics, computer science"

    about = "Hi, my name is " + str(name) + ". I am " + str(age) + " years old. I have a " + str(education) + " I have experience in " + str(specialty) + ". Please speak with me assuming these facts about me."
    intro = call_otherside(about)
    print(intro)

interview()

while True:
    conversation_loop()
    conversation_loop()
    conversation_loop()
    conversation_loop()
    conversation_loop()