from tests.tests import daily_test
from app.google_calendar import GoogleCalendar

if __name__ == '__main__':
    
    # Generate auth token and grant calendar permissions:
    gc = GoogleCalendar(None) # comment or remove after first time running.

    # Run a full system test using the daily test example data.
    #daily_test()