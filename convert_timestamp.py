from datetime import datetime, timezone
import pytz
import re

def extract_timestamp(time_string):

    # Use regular expressions to find the sequence of digits
    timestamp_string = re.search(r'\d+', time_string).group()

    # Convert the extracted string to an integer
    timestamp = int(timestamp_string)

    return timestamp


def convert_timestamp(timestamp_ms):

    # Convert milliseconds to seconds
    timestamp_s = timestamp_ms / 1000.0

    # Create a datetime object from the timestamp in UTC
    dt_utc = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)

    # Define the NZT timezone
    nzt = pytz.timezone('Pacific/Auckland')

    # Convert the UTC datetime to NZT
    dt_nzt = dt_utc.astimezone(nzt)

    # Print the result
    return dt_nzt

def extract_convert_tmstamp(time_string):

    timestamp = extract_timestamp(time_string)
    time = convert_timestamp(timestamp)

    return time


# # Example usage
# date = '/Date(1701303065357)/'
# nzt_time = extract_convert_tmstamp(date)
# print(nzt_time)