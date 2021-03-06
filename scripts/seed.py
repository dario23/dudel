import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dudel import app, db
from dudel.models import Vote, User, Poll, PollType, Choice, VoteChoice
from datetime import datetime, timedelta
import random

vowels = "aeoiu"
consonants = "bcdfghjklmnprstvw"

def random_name():
    length = random.randint(5, 10)
    offset = random.randint(0, 100)
    return "".join([random.choice([vowels, consonants, consonants][(offset+i)%3]) for i in range(length)]).title()

def random_votes(poll, n):
    for x in range(n):
        vote = Vote()
        # vote.name = "Voter %d" % (x+1)
        vote.name = random_name()
        poll.votes.append(vote)

        for choice in poll.choices:
            vote_choice = VoteChoice()
            vote_choice.vote = vote
            vote_choice.choice = choice
            vote_choice.value = random.choice(poll.choice_values.all())

def add_choices(poll, choices):
    for choice in choices:
        poll.choices.append(Choice(choice))

db.drop_all()
db.create_all()

print("Creating user")
user = User()
user.create("13musterm", "Max", "Mustermann", "test@example.com", "hunter2")
db.session.add(user)

print("Creating another user")
user2 = User()
user.create("14musterf", "Minna", "Musterfrau", "test2@example.com", "hunter2")
db.session.add(user2)

print("Creating poll: normal")
poll_normal = Poll("Test: Type Normal", "test-normal", PollType.normal)
poll_normal.owner = user
db.session.add(poll_normal)
add_choices(poll_normal, ["Foo", "Bar", "Baz", "Foobar", "Bazfoo"])
random_votes(poll_normal, 8)

print("Creating poll: datetime")
poll_datetime = Poll("Test: Type Datetime", "test-datetime", PollType.datetime)
poll_datetime.owner = user
db.session.add(poll_datetime)

print("Creating poll: date")
poll_date = Poll("Test: Type Date", "test-date", PollType.date)
poll_date.owner = user
db.session.add(poll_date)
add_choices(poll_date, [datetime.today() + timedelta(days=x) for x in range(5)])

print("Creating poll: large")
poll_large = Poll("Test: Large Poll", "test-large", PollType.normal)
poll_large.owner = user
db.session.add(poll_large)
add_choices(poll_large, [random_name() for i in range(40)])
random_votes(poll_large, 40)

print("Creating poll: autodelete")
poll_autodelete = Poll("Test: Autodelete", "test-autodelete", PollType.normal)
poll_autodelete.owner = user
poll_autodelete.created = datetime.utcnow() - timedelta(days=91)
db.session.add(poll_autodelete)

print("Creating poll: numeric")
poll_numeric = Poll("Test: Type Numeric", "test-numeric", PollType.numeric, create_choice_values=False)
poll_numeric.amount_minimum = 0
poll_numeric.amount_maximum = 2
poll_numeric.amount_step = 0.5
poll_numeric.owner = user
add_choices(poll_numeric, ["Penguins", "Gnus", "Dromedaries", "Pythons"])
db.session.add(poll_numeric)

print("Creating poll: other owner")
poll_owner = Poll("Test: Other owner", "test-owner", PollType.normal)
poll_owner.owner = user2
db.session.add(poll_owner)
add_choices(poll_owner, ["Left", "Right", "Middle"])
random_votes(poll_owner, 20)

db.session.commit()
