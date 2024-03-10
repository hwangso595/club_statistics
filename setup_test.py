# Get the database using the method we defined in pymongo_test_insert file
from db_util import get_database

dbname = get_database()
collection_name = dbname["events"]
collection_name.delete_many({})


events_data = [
    {
        "event_id" : "0",
        "event_name": "Birthday Party",
        "event_location": "Toronto",
        "event_date": "2024-03-15",
        "event_detail": "Celebrating John's 30th birthday with friends and family.",
        "event_people_joined": ["Alice", "Bob", "John", "Eve"]
    },
    {
        "event_id" : "1",
        "event_name": "Conference",
        "event_location": "Toronto",
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
        "event_location": "Vancouver",
        "event_date": "2024-06-05",
        "event_detail": "Live performance by famous rock band 'The Rolling Stones'.",
        "event_people_joined": ["Alice", "David", "Eve", "Frank"]
    }
]
collection_name.insert_many(events_data)