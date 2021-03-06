from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleCalendar:
    def __init__(self, time_scale, schedule=None):
        """ This object serves as an interface between a schedule 
        generated by evoschedule and the Google Calendar API."""
        
        self.time_scale = time_scale
        if time_scale:
            self.weekday_to_date = self.get_weekdays_to_dates()
            self.schedule = schedule
            self.tasks = set(e[2] for e in schedule)
            self.task_color = {task:None for task in self.tasks}
            self.colors = [i for i in range(1, 12)]
        
            i = 0
            for task in self.tasks:
                self.task_color[task] = self.colors[i%11]
                i += 1

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar']


        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'app/credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('calendar', 'v3', credentials=creds)


    def _get_event(self, start, end, name):
        """ Returns the event dictionary required by Calendar API."""

        if self.time_scale == 'daily':
            recurr = "DAILY"
        else:
            recurr = "WEEKLY"
        color = self.task_color[name]

        event = {
            'summary': name,
            'location': '',
            'description': '',
            'start': {
                'dateTime': start,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'America/New_York',
            },
            'recurrence': [
                'RRULE:FREQ='+recurr+';'
            ],
            'colorId' : color
        }
        return event

    def get_weekdays_to_dates(self):
        """ If the time_scale is 'daily' returns the date, 
        otherwise returns a mapping from weekday to date."""

        import datetime

        today = datetime.datetime.today().date()
        num_to_weekday = {
            0 : 'Monday',
            1 : 'Tuesday',
            2 : 'Wednesday',
            3 : 'Thursday',
            4 : 'Friday',
            5 : 'Saturday',
            6 : 'Sunday'
        }
        mapping = {}

        if self.time_scale == 'daily':
            return today.isoformat()
        elif self.time_scale == 'weekly':
            for i in range(7):
                weekday_num = today.weekday()
                mapping[num_to_weekday[weekday_num]] = today.isoformat()
                next_day = datetime.timedelta(days=1)
                today += next_day

        else:
            for i in range(14):
                weekday_num = today.weekday()
                weekday = num_to_weekday[weekday_num]
                if i // 7 == 0:
                    weekday += '1'
                else:
                    weekday += '2'

                mapping[weekday] = today.isoformat()
                next_day = datetime.timedelta(days=1)
                today += next_day
        return mapping


    def convert_day_time_to_datetime(self, day_time):
        """ Takes input in the form Monday,12:00PM and converts to a datetime object."""

        import datetime

        if self.time_scale == 'daily':
            date = self.weekday_to_date # str
        else:
            weekday, day_time = day_time.split(',')
            date = self.weekday_to_date[weekday]
        year, month, day = list(map(int, date.split('-')))

        label = day_time[-2:]
        time = day_time[:-2]
        hour, minute = time.split(':')
        hour, minute = int(hour), int(minute)
        if label == 'PM':
            hour += 12
        elif label == 'AM' and hour == 12:
            hour = 0

        return datetime.datetime(year, month, day, hour, minute)

    def convert_events(self):
        """ Converts a list of events where each event is (start, end, name) 
        where start and end are strings in the form Day,Time to datetime objects."""

        from datetime import datetime, timedelta

        if self.schedule is None:
            raise ValueError("Google Calendar is missing a schedule.")
        if self.time_scale == 'daily':
            offset = timedelta(days=1)
        elif self.time_scale == 'weekly':
            offset = timedelta(days=7)
        else:
            offset = timedelta(days=14)

        converted_schedule = []

        for event in self.schedule:
            start = self.convert_day_time_to_datetime(event[0])
            end = self.convert_day_time_to_datetime(event[1])
            name = event[2]

            # Incase end is bigger
            if start > end:
                end += offset

            start = start.isoformat()
            end = end.isoformat()

            converted_schedule.append((start, end, name))
        converted_schedule.sort()
        return converted_schedule
        
    def simplify_schedule(self, events):
        """ Combines the contiguous time slots of the same task into one time slot. 
        
        This is similar to consolidate_schedule in the GeneSequence class. 
        This method exists because when we convert events from Day,Time strings to 
        datetime objects, new contiguous time slots of the same task can form."""

        n = len(events)
        task = events[0][2]
        start = events[0][0]
        combined_events = []
        for i in range(n):
            if events[i][2] != task:
                end = events[i][0]
                if task != 'Free':
                    combined_events.append((start, end, task))
                task = events[i][2]
                start = events[i][0]
        end = events[n-1][1]
        if task != 'Free':
            combined_events.append((start, end, task))
        return combined_events
        
    def add_events(self):
        """ Iterates through the events and adds them one by one to the user's 
        google calendar."""

        from time import sleep
        from tqdm import tqdm

        converted_schedule = self.convert_events()
        schedule = self.simplify_schedule(converted_schedule)
        for event in tqdm(schedule):
            start, end, name = event
            #print(start, end, name)
            gc_event = self._get_event(start, end, name)
            self.service.events().insert(calendarId='primary', body=gc_event).execute()
            sleep(0.1)