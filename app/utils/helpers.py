from datetime import datetime
from dateutil import parser

def convert_iso_to_readable_time(iso_string):
    """Convert ISO 8601 datetime to a readable time format (12-hour with AM/PM)."""
    dt = parser.isoparse(iso_string)  
    return dt.strftime("%I:%M %p")  