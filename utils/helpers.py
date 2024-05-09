from datetime import datetime

def reformat_datetime(datetime_str):
    parsed_datetime = datetime.strptime(datetime_str, '%d %b %Y %H:%M')
    return parsed_datetime

# i kinda confuse about the condition, so i will just leave the reformat function in case user input different format
# List of possible datetime formats
    # datetime_formats = [
    #     '%b %d %H:%M:%S %Y',
    #     '%d/%m/%Y %H:%M:%S',
    #     # Add more formats as needed
    # ]
    
    # # Attempt to parse the timestamp using each format
    # for format_str in datetime_formats:
    #     try:
    #         dt = datetime.strptime(timestamp_str, format_str)
    #         # Format the datetime object and return it
    #         formatted_datetime = dt.strftime('%d %b %Y %H:%M')
    #         return formatted_datetime
    #     except ValueError:
    #         # If parsing fails, try the next format
    #         continue
    
    # # If none of the formats match, raise an error
    # raise ValueError("Invalid timestamp format")
