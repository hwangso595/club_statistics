from taipy.gui import Gui, navigate, notify
from db_util import get_database
from app import get_app, get_user
from flask import session

root_md_admin="<|menu|label=Menu|lov={[('Page-1', 'Page 1'), ('Page-2', 'Page 2'), ('/logout', 'Log Out')]}|on_action=on_menu|>"
root_md_user="<|menu|label=Menu|lov={[('Page-1', 'Page 1'), ('/logout', 'Log Out')]}|on_action=on_menu|>"

user_type = ""
user_name = ""


# ============================================= page 1 =============================================
db = get_database()
events_data = list(db['events'].find())

# Sample user

def event_to_table():
    events ={
        "event id":  [event["event_id"] for event in events_data],
        "event date" : [event["event_date"] for event in events_data],
        "event detail":[event["event_detail"] for event in events_data],
        "event location": [event["event_location"] for event in events_data],
        "event name": [event["event_name"] for event in events_data],
        "event people joined": [len(event["event_people_joined"]) for event in events_data],

    }
    return events

events = event_to_table()

column_orders = [("event date; event id;event name;event location;event detail;event people joined", "By event date"), ("event people joined;event id; event name;event detail;event date", "BY people")]
columns = column_orders[0]

page1_md = """
<|{events}|table|columns={columns[0]}|show_all|rebuild|>

<|{columns}|toggle|lov={column_orders}|>
<|{value}|input|on_change=update_id|>
"""

def update_id(state):
    if user_type == "admin":
        for index, event in enumerate(events["event id"]):
            if str(event) == state.value:
                state.name = events["event name"][index]
                state.detail = events["event detail"][index]
                state.date = events["event date"][index]
                state.location = events["event location"][index]

value = "Enter event id"
def add_user(state):
    for index, event in enumerate(events_data):
        if str(event["event_id"])== state.value:
            if user_name not in event["event_people_joined"]:
                event["event_people_joined"].append(user_name)
                notify(state,"info", "You have successfully joined the event")
            else:
                notify(state,"info","You have already joined")
            print(event)
            break

    state.events = event_to_table()


def remove_user(state):
    for index, event in enumerate(events_data):
        if str(event["event_id"]) == state.value:
            if user_name in event["event_people_joined"]:
                event["event_people_joined"].remove(user_name)
                notify(state, "info", "You have successfully unjoined the event")
            else:
                notify(state, "info", "You have not joined")
            print(event)
            break

    state.events = event_to_table()


def add_event(state):
    modified = 0
    for index, event in enumerate(events_data):
        if str(event["event_id"]) == state.value:
            events_data[index]["event_name"] = state.name
            events_data[index]["event_date"] = state.date
            events_data[index]["event_detail"] = state.date
            events_data[index]["event_location"] = state.location
            notify(state, "info", "You have successfully add/modified the event")
            modified = 1
            break
    if modified == 0:
        events_data.append({"event_name": state.name, "event_date": state.date, "event_detail": state.detail, "event_id": state.value, "event_people_joined": []})
    state.events = event_to_table()

def remove_event(state):
    for index, event in enumerate(events_data):
        if str(event["event_id"]) == state.value:
            events_data.pop(index)
            notify(state, "info", "You have successfully removed the event")
            break

    state.events = event_to_table()


name ="name"
detail= "detail"
date = "date"
location = "location"


# ==================================================================================================

# ============================================= page 2 =============================================
sorted(events_data, key=lambda x: x['event_date'])


def event_to_table(events_data):
    events ={
        "event id":  [event["event_id"] for event in events_data],
        "event date" : [event["event_date"] for event in events_data],
        "event detail":[event["event_detail"] for event in events_data],
        "event location": [event["event_location"] for event in events_data],
        "event name": [event["event_name"] for event in events_data],
        "event people joined": [len(event["event_people_joined"]) for event in events_data],
        "event people name": [event["event_people_joined"] for event in events_data],

    }
    return events

events = event_to_table(events_data)

min_event =0
max_event = len(events["event date"])-1


slider_min = 0
slider_max = max_event
page2_md = """
<|{slider_min}|slider|min={min_event}|max={max_event}|><|{slider_max}|slider|min={min_event}|max={max_event}|>

Event people joined vs date
<|{events}|chart|x=event date|y[1]=event people joined|> Frequency of # of people joined event <|{events}|chart|type=histogram|y=event people joined|>
"""


def on_change(state, var_name: str, var_value):
    if var_name == "slider_min":
        if state.slider_max < state.slider_min:
            state.slider_max = state.slider_min

    if var_name == "slider_max":
        if state.slider_max < state.slider_min:
            state.slider_min = state.slider_max

    state.events = event_to_table(events_data[state.slider_min: state.slider_max])

# ==================================================================================================

# ============================================= Home =============================================


homepage = """
<|{user_name}|input|>

<|Login As User|button|on_action=on_login|>  <|Login As Admin|button|on_action=on_login_admin|>
"""


# Gui(page2_md).run(use_reloader=True)

def on_login(state):
    user_type = "user"
    user_name=state.user_name
    navigate(state, to="Page-1")

def on_login_admin(state):
    user_type = 'admin'
    user_name = state.user_name
    navigate(state, to="Page-1")

def on_logout(state):
    user_type = 'none'
    navigate(state, to="Page-1")

# homepage = """
# # Welcome to Club Statistics App

# This app allows you to log in as an owner or a customer and view club statistics.

# To access the app, you can log in as an owner or a customer. Click on the respective buttons below:

# Enjoy using the Club Statistics App!

# """ + "<|Log In as Admin|button|on_action=on_login_admin|> <|Log In as Customer|button|on_action=on_login|> "

# ==================================================================================================

    def on_menu(state, action, info):
        page = info["args"][0]
        navigate(state, to=page, force=True, tab='_self')

if user_type == "user":
    page1_md += "<|Join event|button|on_action=add_user|><|Unjoin event|button|on_action=remove_user|>"
    pages = {
        "Page-3": homepage,
        "/": root_md_user,
        "Page-1": page1_md,
        "logout": "<|Logout|on_action=on_logout|>"
    }
else:
    page1_md += "<|{name}|input|> <|{detail}|input|><|{date}|input|><|{location}|input|><|Add/Edit event|button|on_action=add_event|><|Remove event|button|on_action=remove_event|>"

    pages = {
        "Page-3": homepage,
        "/": root_md_admin,
        "Page-1": page1_md,
        "Page-2": page2_md,
        "logout": "<|Logout|on_action=on_logout|>"
    }

Gui(pages=pages).run(use_reloader=True)