from taipy.gui import Gui,notify
# Sample data of events and user participation
events_data = [
    {
        "event_id" : "0",
        "event_location": "Toronto",
        "event_name": "Birthday Party",
        "event_date": "2024-03-15",
        "event_detail": "Celebrating John's 30th birthday with friends and family.",
        "event_people_joined": ["Alice", "Bob", "John", "Eve"]
    },
    {
        "event_id" : "1",
        "event_location": "Toronto",
        "event_name": "Conference",
        "event_date": "2024-04-20",
        "event_detail": "Tech conference showcasing latest innovations in AI and robotics.",
        "event_people_joined": ["Alice", "Charlie"]
    },
    {
        "event_id" : "2",
        "event_name": "Workshop",
    "event_location": "Toronto",
        "event_date": "2024-05-10",
        "event_detail": "Hands-on workshop on web development using Python and Django.",
        "event_people_joined": ["Bob", "David", "Eve"]
    },
    {
        "event_id" : "3",
        "event_name": "Music Concert",
        "event_location": "Toronto",
        "event_date": "2024-06-05",
        "event_detail": "Live performance by famous rock band 'The Rolling Stones'.",
        "event_people_joined": ["Alice", "David", "Eve", "Frank"]
    }
]

# Sample user
user_name = "Eve"
user_type ="user"

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
user_type = 'user'
if user_type == "user":
    page1_md += "<|Join event|button|on_action=add_user|><|Unjoin event|button|on_action=remove_user|>"

if user_type == "admin":
    page1_md += "<|{name}|input|> <|{detail}|input|><|{date}|input|><|{location}|input|><|Add/Edit event|button|on_action=add_event|><|Remove event|button|on_action=remove_event|>"

Gui(page1_md).run()