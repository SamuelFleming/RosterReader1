from pyicloud import PyiCloudService
import pandas as pd
from datetime import datetime, timedelta

# Authenticate with iCloud
# Replace 'your-apple-id' with your actual Apple ID

apple_id = "flemo1485@gmail.com"
apple_pass = "Nancy-01"


api = PyiCloudService(apple_id = apple_id, password=apple_pass)


# Handle Two-Factor Authentication
if api.requires_2fa:
    print("\n\n Requries the authentication")
    code = input("Enter the 2FA code you received: ")
    result = api.validate_2fa_code(code)
    print("2FA Code validated successfully." if result else "Failed to validate 2FA code.")

if not api.is_trusted_session:
    print("\n\nSession not trusted. Please approve this session in your iCloud settings.")
    exit(1)
else:
    print("session is trusted. Now what?")

# # Function to fetch 'Work' events from Apple Calendar
# def get_work_events(api):
#     work_events = []
    
#     # Get the calendar events
#     calendars = api.calendar.events()
    
#     # Filter and collect work events
#     for event in calendars:
#         # Check if the event has the 'Work' label
#         if 'work' in event.get('title', '').lower() and event['type'] == 'event':
#             start_time = datetime.strptime(event['startDate'][0:19], "%Y-%m-%dT%H:%M:%S")
#             end_time = datetime.strptime(event['endDate'][0:19], "%Y-%m-%dT%H:%M:%S")
#             work_events.append({
#                 'date': start_time.date(),
#                 'start_time': start_time.time(),
#                 'end_time': end_time.time()
#             })

#     return work_events

# # Fetch the work events
# events = get_work_events(api)

# Print out available calendars
calendars = api.calendar.events()  # This lists all calendars associated with the account
print("Available Calendars:", calendars)

# Fetch events and print them out
events = api.calendar.events(from_dt=datetime.now() - timedelta(days=30), to_dt=datetime.now() + timedelta(days=30))
for event in events:
    print(event)

# Convert the list of events to a pandas DataFrame
df = pd.DataFrame(events)

# Display the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
df.to_csv('work_shifts.csv', index=False)