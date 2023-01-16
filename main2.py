import datetime
from cal_setup import get_calendar_service
from googleapiclient.discovery import build
import pytz
from finding_workout import create_workout


user_input = input("How many weeks would you like this to be in your calendar? ")
recurrence = 'RRULE:FREQ=WEEKLY;COUNT={}'.format(user_input)
days_of_week_dict = {0:"Monday", 1: "Tuesday", 2: "Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}

#T0D0
#comments/go through code:
#select workout type for day 1:


def main():
    service = get_calendar_service()
    calendar_id = create_calendar(service)
    calendar_info = service.calendarList().get(calendarId=calendar_id).execute()
    calender_id = (calendar_info['id'])
    link = f'https://calendar.google.com/calendar/embed?src={calendar_id}'
    print(link)

    days_of_week = input("Which days of the week would you like to workout? (e.g. 0, 1, 2 for Monday, Tuesday, Wednesday) ")
    days_of_week = days_of_week.split(',')
    days_of_week = [int(day) for day in days_of_week]  # convert the input to a list of integers'
    


    for day in days_of_week:
        day_workout = input("Choose muscle group for day {}: Options are Chest, Arms, Legs, BodyWeight  ".format(day))
        time_of_day = input(f"What time on {days_of_week_dict[day]} would you like the workout to be? (e.g. 09:00 for 9am) ")

        #call function to show available times so the user can see:
        time_of_event = datetime.datetime.strptime(time_of_day, "%H:%M")
        utc_time = datetime.datetime.utcnow()
        eastern = pytz.timezone('US/Eastern')
        now = utc_time.astimezone(eastern)
        # Find the number of days until the next Monday
        days_until_day = 7 - now.weekday()
        if days_until_day <= 0:
            days_until_day += 7
        start_time = eastern.localize(datetime.datetime.combine(now + datetime.timedelta(days=days_until_day + day), time_of_event.time()))
        end_time = start_time + datetime.timedelta(hours=1)
        add_event(service, calendar_id, 'Workout', day_workout, start_time.isoformat(), end_time.isoformat())

    # This function will create a calendar and return the calendar's ID
def create_calendar(service):
    calendar = {
        'summary': 'Workout Calendar',
        'timeZone': 'UTC',
        'visibility': 'public',
        'accessRole': 'owner' #public
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    print(f'Calendar created: {created_calendar.get("summary")}')
    return created_calendar.get('id')



# This function will add an event to the calendar
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