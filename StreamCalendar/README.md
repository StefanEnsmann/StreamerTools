# Stream Calendar
A simple visualization for stream schedules based on Google calendar.

## Features
- [x] Fetch dates from a google calendar
- [x] Display dates ordered by year, month and day
- [x] Show the next date on top
- [x] List members of a team with individual colors and images
- [x] Support for recurring events

## Usage
Upload the files to a webspace of your choice. Additionally provide two files in the root directory (where index.html is) as follows:

### calendar_info.js
Find your calendar id in your Google calendar settings. Create an API key via the Google developer console.
```javascript
var calendar_id = "abcdefghijklmnop@1234567890.com";
var api_key = "ABCdefGHIjklMNOpqrSTUwxyZ";
```

### streamers.json
Define the list of streamers given their display name, background and font color as well as an image URL. This calendar supports members of a core team as well as "friends" in a separate list.
```javascript
{
    "crew": {
        "name_1": {
            "bg": "#FF69B4", "font": "#F0F0FF", "dis": "Name_1",
            "pic": "https://link_to_image_2.png"
        },
        "name_2": {
            "bg": "#FF69B4", "font": "#F0F0FF", "dis": "naME_2",
            "pic": "https://link_to_image_2.png"
        },
    },
    "friends": {
        "friend_1": {
            "bg": "#FF69B4", "font": "#F0F0FF", "dis": "Friend_NAME_1",
            "pic": "https://link_to_image_image_3.png"
        }
    }
}
```

### Event format
Due to historical reasons the event format in Google calendar is as follows:
- Event name contains the name of the streamer. Does not need to match one from streamers.json
- Event description contains the name of the event
- Event location may optionally contain a link which is made clickable
  
Old events do not need to be cleared. This application only loads the events for the current month and loads additional months on demand when they are opened. It may load future months on startup to fill the "Next up" field, if the current month only contains past events.