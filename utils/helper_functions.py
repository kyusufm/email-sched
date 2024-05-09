from datetime import datetime

def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, '%d %b %Y %H:%M')