import datetime
from .colour import Colour


def print_connection_error(error_count):
    if (error_count < 3):
        print(f"{Colour().error} Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')} {Colour().default}")
        error_count += 1
        return error_count
    elif (error_count == 3):
        print(f"{Colour().error} Connection error persisting... Check connection {Colour().default}")
        error_count += 1
        return error_count
    else:
        error_count += 1
        return error_count
