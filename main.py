#PROJECT TITLE: WORKOUT GENERATOR USING GOOGLE API's 
#AUTHOR: Jacob Albert
#DESCRIPTION:
    #CREATING CALENDAR USING GOOGLE API:
        #uses google calendar API to create a calendar used for the workout. In this case, the
        #calender created is shareable, so anyone with the link can use the calendar.
    #GETTING USER DATA:
        #asks user for information about the workout including how many days they would 
        #like to workout, which days of the week, which times, and what type of workout
        #i.e (Chest, Arms, Back etc)
    #CREATING WORKOUT:
        #takes input data and creates personalized workout based on the information provided
        #it then uses this workout as the description for the calendar event, along with other relevant information

#relevant files: main, finding_workout.py, cal_setup.py


#import libaries necessary
import datetime
from cal_setup import get_calendar_service
from googleapiclient.discovery import build
import pytz
from finding_workout import create_workout

user_input = input("How many weeks would you like this to be in your calendar? ")

#choose how many weeks would you like each workout to repeat for
recurrence = 'RRULE:FREQ=WEEKLY;COUNT={}'.format(user_input)
days_of_week_dict = {0:"Monday", 1: "Tuesday", 2: "Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}



def main():
    service = get_calendar_service()
    calendar_id = create_calendar(service)
    calendar_info = service.calendarList().get(calendarId=calendar_id).execute()
    calender_id = (calendar_info['id'])
    link = f'https://calendar.google.com/calendar/embed?src={calendar_id}'
    #printing the link to download the workout:
    print(link)

    days_of_week = input("Which days of the week would you like to workout? (e.g. 0, 1, 2 for Monday, Tuesday, Wednesday) ")
    days_of_week = days_of_week.split(',')
    days_of_week = [int(day) for day in days_of_week]  # convert the input to a list of integers
    


    for day in days_of_week:
        day_workout = input("Choose muscle group for day {}: Options are Chest, Arms, Back, Legs  ".format(day))
        time_of_day = input(f"What time on {days_of_week_dict[day]} would you like the workout to be? (e.g. 09:00 for 9am) ")
        time_of_event = datetime.datetime.strptime(time_of_day, "%H:%M")
        utc_time = datetime.datetime.utcnow()
        #convert from UTC time to eastern time
        eastern = pytz.timezone('US/Eastern')
        now = utc_time.astimezone(eastern)
        # Find the number of days until the workout specified: 
        days_until_day = 7 - now.weekday()
        if days_until_day <= 0:
            days_until_day += 7
        start_time = eastern.localize(datetime.datetime.combine(now + datetime.timedelta(days=days_until_day + day), time_of_event.time()))
        end_time = start_time + datetime.timedelta(hours=1)
        add_event(service, calendar_id, 'Workout', day_workout, start_time.isoformat(), end_time.isoformat())

    #create a calendar and return the calendar's ID
def create_calendar(service):
    calendar = {
        'summary': 'Jacob Sample Workout Calendar',
        'timeZone': 'UTC',
        #make sure the calendar is public so can be shared
        'visibility': 'public',
        'accessRole': 'owner' 
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    print(f'Calendar created: {created_calendar.get("summary")}')
    return created_calendar.get('id')



# Add an event to the calendar
def add_event(service, calendar_id, summary, des, start_time, end_time):
    workout_string = create_workout(des)
    event = {
        'summary': summary,
        'description': workout_string,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
        'recurrence': [recurrence],
        'visibility': 'public'
    }
    service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'Event added: {summary}')


if __name__ == '__main__':
   main()
