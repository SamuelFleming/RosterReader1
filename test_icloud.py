
from env_setup import ensure_environment, activate_and_run_in_environment

env_name = "icloud_env"
script_path = __file__  # Get the current script path

# Ensure the environment is set up and activated if it exists
ensure_environment(env_name=env_name)

# Now continue with your iCloud API functionality
from pyicloud import PyiCloudService
import datetime
from datetime import timedelta
import pandas as pd

# iCloud credentials
apple_id = "flemo1485@gmail.com"
apple_pass = "Nancy-01"

# Initialize the iCloud service
api = PyiCloudService(apple_id=apple_id, password=apple_pass)

# Clear session and cookie data manually
api.session.cookies.clear()
api.session_data.clear()
api.authenticate(force_refresh=True)

print("Session Token:", api.session_data.get("session_token"))
print("Is Trusted Session:", api.is_trusted_session)
print("Requires 2FA:", api.requires_2fa)
print("Requires 2SA:", api.requires_2sa)

cal_auth = False

try:
    api.authenticate(force_refresh=True, service="calendar")
    print("Calendar service is authenticated")
    cal_auth = True
except Exception as e:
    print(f"Error authenticating calendar service: {e}")

try:
    service_url = api._get_webservice_url("calendar")
    print(f"Calendar Service URL: {service_url}")
except Exception as e:
    print(f"Calendar service not activated or available: {e}")

try:
    calendars = api.calendar.calendars()
except Exception as e:
    print(f"Failed to fetch calendar events: {e}")
    print("API Response:", e.response.text if hasattr(e, 'response') else "No response text available")

try:
    contacts = api.contacts.all()
    print("Contacts fetched successfully")
except Exception as e:
    print(f"Failed to fetch contacts: {e}")

# Handle Two-Factor Authentication
   
if api.requires_2fa:
    print("\n\n Requires authentication")
    code = input("Enter the 2FA code you received: ")
    result = api.validate_2fa_code(code)
    print("2FA Code validated successfully." if result else "Failed to validate 2FA code.")

if not api.is_trusted_session:
    print("\n\nSession not trusted. Please approve this session in your iCloud settings.")
else:
    print("Session is trusted. Now what?\n\nLet's see what services are authenticated?")

try:
    calendars = api.calendar.calendars()
    print(f"\n\nCalendars fetched successfully: {calendars}\n")
except Exception as e:
    print(f"Failed to fetch calendar events: {e}")
    print("API Response:", e.response.text if hasattr(e, 'response') else "No response text available")

try:
    contacts = api.contacts.all()
    print(f"\n\nContacts fetched successfully: \n")
    for contact in contacts:
        print(contact)
except Exception as e:
    print(f"Failed to fetch contacts: {e}")

# Fetch events and print them out
events = api.calendar.events()
for event in events:
    print(event)



